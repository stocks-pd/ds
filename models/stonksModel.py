from abc import ABCMeta, abstractmethod
import pandas as pd
import numpy as np
from models.our_prophet import OurProphet
import multiprocessing as mp


class StonksModel(metaclass=ABCMeta):
    def __init__(self, company_ticket: str, api_key: str = "ZRMG7N7CVNEFA2RY"):
        """

        :param company_ticket:
        :param api_key:
        """
        self.api_key = api_key
        self.company_ticket = company_ticket.upper()

        self.model = None

        self.data_to_fit = self.preprocessing(self.get_data_from_api(company_ticket, api_key))

        # заданы на 3 года обучения и 1 год предсказания
        self._train_size = 756
        self._test_size = 252

        self.forecast = None
        # self.forecast_period = None
        self.best_prophet = None
        self.best_hyper_parameters = None
        self.learned_prophets = None

        # metrics
        self.rmse = None
        self.mape = None
        self.mae = None

    @staticmethod
    def get_data_from_api(company_ticket, api_key):
        """

        :param company_ticket:
        :param api_key:
        :return:
        """
        query = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}' \
                '&outputsize=full&apikey={}&datatype=csv'.format(company_ticket, api_key)
        return pd.read_csv(query)

    @staticmethod
    def preprocessing(df):
        """

        :param df:
        :return:
        """
        newDataFrame = pd.DataFrame(columns=["ds", "y"])
        newDataFrame.ds = pd.to_datetime(df.timestamp)
        newDataFrame.y = df.close
        return newDataFrame

    def fit(self, data: pd.DataFrame, n_changepoints: int = None, changepoint_prior_scale: float = None,
            changepoint_range: float = None, fourier_order: int = None):
        """
        :param data:
        :param n_changepoints:
        :param changepoint_prior_scale:
        :param changepoint_range:
        :param fourier_order:
        :return:
        """
        self.model = OurProphet(daily_seasonality=True, n_changepoints=n_changepoints,
                                changepoint_prior_scale=changepoint_prior_scale,
                                changepoint_range=changepoint_range)
        self.model.add_seasonality(name='monthly', period=21, fourier_order=fourier_order)
        self.model.fit(data)

    def predict(self, periods: int = 90, freq="D", include_history=False):
        """

        :param periods:
        :param freq:
        :param include_history:
        :return:
        """
        future = self.model.make_future_dataframe(periods, freq, include_history)
        self.forecast = self.model.predict(future)

    @staticmethod
    def get_rmse(y: np.array, y_pred: np.array):
        """

        :param y:
        :param y_pred:
        :return:
        """
        return np.sqrt(np.mean((y - y_pred) ** 2))

    @staticmethod
    def get_mape(y: np.array, y_pred: np.array):
        """

        :param y:
        :param y_pred:
        :return:
        """
        return np.mean((y - y_pred) / y) * 100

    @staticmethod
    def get_mae(y: np.array, y_pred: np.array):
        """

        :param y:
        :param y_pred:
        :return:
        """
        return np.mean(np.abs(y - y_pred))

    # def get_metrics_sum(self, y, y_pred):
    #     return self.get_mape(y, y_pred) + self.get_rmse(y, y_pred) + self.get_mae(y, y_pred)

    # TODO: придумать как задавать интервал, из которого выбираются гиперпараметры
    @staticmethod
    def _create_dict_of_hyperparameters_with_values():
        hyperparameters_combined = []
        hyperparameters_dict = {
            "n_changepoints": [i for i in range(0, 210, 40)],
            "changepoint_prior_scale": [i / 100 for i in range(0, 250, 50)],
            "changepoint_range": [i / 100 for i in range(0, 100, 20)],
        }
        for n_changepoints in hyperparameters_dict.get("n_changepoints"):
            for changepoint_prior_scale in hyperparameters_dict.get("changepoint_prior_scale"):
                for changepoint_range in hyperparameters_dict.get("changepoint_range"):
                    hyperparameters_combined.append({"n_changepoints": n_changepoints,
                                                     "changepoint_prior_scale": changepoint_prior_scale,
                                                     "changepoint_range": changepoint_range})
        return hyperparameters_combined

    def _fit_predict_with_get_metrix_score_to_update_hyperparameters(self, item):
        """

        :param item:
        :return:
        """
        train_data = self.data_to_fit[self._test_size:self._test_size + self._train_size]
        test_data = self.data_to_fit[:self._test_size]
        prophet = OurProphet(n_changepoints=item.get("n_changepoints"),
                             changepoint_prior_scale=item.get("changepoint_prior_scale"),
                             changepoint_range=item.get("changepoint_range"))
        prophet.add_seasonality(name='monthly', period=21, fourier_order=3)
        prophet.fit(train_data)
        future = prophet.make_future_dataframe(periods=self._test_size, freq='D', include_history=True)
        forecast = prophet.predict(future)
        rmse = self.get_rmse(test_data.to_numpy(), forecast.yhat.to_numpy())
        return {"prophet": prophet, "rmse": rmse}

    def get_best_hyperparameter_and_prophet(self):
        """

        :return: pass
        """
        # TODO: дополнить список гиперпараметров
        hyperparameters_combined = self._create_dict_of_hyperparameters_with_values()

        pool = mp.Pool()

        self.learned_prophets = pool.map(self._fit_predict_with_get_metrix_score_to_update_hyperparameters,
                                         hyperparameters_combined)

        self.learned_prophets.sort(key=lambda prophet: prophet.get("rmse"))
        self.best_prophet = self.learned_prophets[0].get("prophet")
        self.best_hyper_parameters = self.best_prophet.get_hyperparameters()

    @abstractmethod
    def get_best_prediction(self):
        return
