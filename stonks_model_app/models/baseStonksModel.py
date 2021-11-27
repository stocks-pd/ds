from abc import ABCMeta
import pandas as pd
import numpy as np
from stonks_model_app.app_settings import *

from stonks_model_app.models.estimators.our_prophet import OurProphet


class BaseStonksModel(metaclass=ABCMeta):
    def __init__(self, estimator: str = "OurProphet", api_key: str = ALPHA_KEY):
        """

        :param company_ticker:
        :param api_key:
        """
        self.api_key = api_key
        self.estimators_dict = {"OurProphet": OurProphet}
        try:
            self.estimator = self.estimators_dict.get(estimator)
        except KeyError:
            raise Exception("Указан неверный тип модели")

    @staticmethod
    def get_data_from_api(company_ticker, api_key):
        """

        :param company_ticker:
        :param api_key:
        :return:
        """
        query = ALPHA_GET_TIKER_HISTORY.format(company_ticker, api_key)
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

    def fit(self, data, parameters):
        """
        :param data:
        :param n_changepoints:
        :param changepoint_prior_scale:
        :param changepoint_range:
        :param fourier_order:
        :return:
        """
        self.model = self.estimator(**parameters)
        self.model.add_seasonality(name='monthly', period=21, fourier_order=3)
        self.model.add_seasonality('quarterly', period=63, fourier_order=8)
        self.model.add_country_holidays(country_name='US')
        self.model.fit(data)

    def predict(self, periods: int = 90, freq="D", include_history=False):
        """

        :param periods:
        :param freq:
        :param include_history:
        :return:
        """
        future = self.model.make_future_dataframe(periods, freq, include_history)
        return self.model.predict(future)

    def fit_predict(self, data, parameters, periods: int = 90, freq="D", include_history=False):
        self.fit(data, parameters)
        return self.predict(periods, freq, include_history)

    @staticmethod
    def get_smape(y: np.array, y_pred: np.array):
        """
        Выдает значения метрики sMAPE
        :param y:
        :param y_pred:
        :return:
        """
        return np.mean(2 * abs(y - y_pred) / (y + y_pred)) * 100
