from stonks_model_app.models.estimators.interfaces.imodel import IModel
from abc import ABCMeta, abstractmethod
import pandas as pd


class BaseModelSelection(metaclass=ABCMeta):
    def __init__(
            self,
            estimator: IModel,
            param_grid: dict,
            scoring=None,
            n_jobs=None
    ):
        self.estimator = estimator
        self.param_grid = param_grid
        self.scoring = scoring
        self.n_jobs = n_jobs

        self.learned_models: dict = None

    @abstractmethod
    def fit(self, data: pd.DataFrame, future_period: int):
        pass

    @abstractmethod
    def find_best_parameters(self):
        pass


    # def get_best_parameters(self, data: pd.DataFrame, estimator: str, forecast_period: int):
    #     train_data = data.iloc[forecast_period:]
    #     test_data = data.iloc[:forecast_period]
    #
    #     pool = mp.Pool()
    #
    #     param_grid = [dict(zip(self.estimators_dict.keys(), v, train_data, test_data)) for v in
    #                   itertools.product(*self.estimators_dict.values())]
    #     print(param_grid)
    #     # param_grid = model.get_params_grid(self.estimators_dict, train_data, test_data)
    #     #
    #     # learned_models = pool.map(self._fit_predict_with_get_metrix_score_to_update_hyperparameters,
    #     #                           param_grid)
    #     #
    #     # learned_models.sort(key=lambda prophet: prophet.get("metric"))
    #     #
    #     # return best_params

    # def _fit_predict_with_get_metrix_score_to_update_hyperparameters(self, item):
    #     """
    #
    #     :param item:
    #     :return:
    #     """
    #     estimator = item.pop("estimator")
    #     train_data = item.pop("train_data")
    #     test_data = item.pop("test_data")
    #     model = estimator(**item)
    #     model.add_seasonality(name='monthly', period=21, fourier_order=3)
    #     model.add_seasonality('quarterly', period=63, fourier_order=8)
    #     model.add_country_holidays(country_name='US')
    #     model.fit(train_data)
    #
    #     future = model.make_future_dataframe(test_data.shape[0])
    #     forecast = model.predict(future)
    #     smape = self.get_smape(test_data.y, forecast.y)
    #
    #     return {"prophet": model, "metric": smape}