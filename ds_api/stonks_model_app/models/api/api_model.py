from multiprocessing import Pool
from ..baseStonksModel import BaseStonksModel
from ...app_settings import *


class ApiBaseStonksModel(BaseStonksModel):
    def __init__(self, estimator: str = "OurProphet", api_key: str = "ZRMG7N7CVNEFA2RY"):
        BaseStonksModel.__init__(self, estimator, api_key)

    def fit_predict_transform(self, data, parameters, periods: str, freq="D", include_history=False, to_rec=False):
        print(periods)
        period_types = {
            "WEEK": WEEK,
            "MONTH": MONTH,
            "QUART": QUART,
            "HALF_YEAR": HALF_YEAR,
            "YEAR": YEAR
        }
        periods = period_types.get(periods)
        print(periods)
        risk = BaseStonksModel.fit_predict(self, data.iloc[periods:], parameters, periods)
        risk = round(self.get_smape(data.loc[:periods, ['y']].to_numpy(), risk.yhat.to_numpy()), 2)
        print(risk)
        predict = BaseStonksModel.fit_predict(self, data, parameters, periods)
        predict["risk"] = risk
        if to_rec:
            return {
                'price': predict.loc[-1, ["yhat"]],
                'risk': predict.loc[-1, ["risk"]]
            }
        else:
            return predict[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'risk']].to_json(orient="records")

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
