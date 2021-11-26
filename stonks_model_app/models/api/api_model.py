from stonks_model_app.models.baseStonksModel import BaseStonksModel
import multiprocessing as mp
import pandas as pd


class ApiBaseStonksModel(BaseStonksModel):
    def __init__(self, estimator: str = "OurProphet", api_key: str = "ZRMG7N7CVNEFA2RY"):
        BaseStonksModel.__init__(self, estimator, api_key)

        # self.param_grid = self.model.get_params_grid()

    def fit_predict(self, data, parameters, periods: int = 90, freq="D", include_history=False, to_rec=False):
        period_types = {
            "week": 5,
            "month": 21,
            "quarter": 63,
            "half_year": 126,
            "year": 252
        }
        if isinstance(periods, str):
            periods = period_types.get(periods)

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
            return predict[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'risk']].to_json()
