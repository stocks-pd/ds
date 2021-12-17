from multiprocessing import Pool
from ..baseStonksModel import BaseStonksModel
from ...app_settings import *
import pandas as pd


class ApiBaseStonksModel(BaseStonksModel):
    def __init__(self, estimator: str = "OurProphet", api_key: str = "ZRMG7N7CVNEFA2RY"):
        BaseStonksModel.__init__(self, estimator, api_key)

    def fit_predict_transform(self, data, parameters, periods: str, freq="D", include_history=False, to_rec=False):
        period_types = {
            "WEEK": WEEK,
            "MONTH": MONTH,
            "QUART": QUART,
            "HALF_YEAR": HALF_YEAR,
            "YEAR": YEAR
        }
        periods = period_types.get(periods)
        smape = BaseStonksModel.fit_predict(self, data.iloc[periods:], parameters, periods)
        smape = round(self.get_smape(data.loc[:periods, ['y']].to_numpy(), smape.yhat.to_numpy()), 2)
        print(smape)
        predict = BaseStonksModel.fit_predict(self, data, parameters, periods)
        predict['yhat'] = predict['yhat'].apply(round(2))
        predict['yhat_lower'] = predict['yhat_lower'].apply(round(2))
        predict['yhat_upper'] = predict['yhat_upper'].apply(round(2))
        predict['ds'] = predict['ds'].dt.strftime('%Y-%m-%d')
        if to_rec:
            return {
                'price': predict.loc[-1, ["yhat"]],
                'risk': predict.loc[-1, ["risk"]]
            }
        else:
            return predict[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_json(orient="records"), smape

    def double_selection_hyperparameters(self, tiker, periods=QUART):
        best_params = self._complete(tiker, periods)
        self._reorganization(best_params)
        final_params = self._complete(tiker, periods, False)
        return final_params

    def _complete(self, tiker, periods, logic_params_type=True):
        data = self.get_data(tiker, self.api_key)
        train_ts, test_ts = self.train_test_split(data, periods=periods)

        params_grid = self.estimator.get_params_grid(train_ts, test_ts, logic_params_type)

        pool = Pool(processes=PERMISSIBLE_CPU_COUNT)
        scored_params = pool.map(self._scoring_model, params_grid)
        scored_params.sort(key=lambda x: x.get('score'))
        return scored_params[0].get('params')

    def _scoring_model(self, item):
        train = item.pop('train')
        test = item.pop('test')
        forecast = self.fit_predict(train, item, test.shape[0])
        score = self.get_smape(test.y.to_numpy(), forecast.yhat.to_numpy())
        print(item)
        return {'score': score, 'params': item}

    @staticmethod
    def _reorganization(dict):
        for i in dict.items():
            dict[i[0]] = [i[1]]
