from abc import ABCMeta, abstractmethod
import pandas as pd
import numpy as np

from stonks_model.src.models.our_prophet import OurProphet
import multiprocessing as mp
import itertools


class StonksModel(metaclass=ABCMeta):
    def __init__(self, company_ticker: str, api_key: str = "ZRMG7N7CVNEFA2RY"):
        """

        :param company_ticker:
        :param api_key:
        """
        self.api_key = api_key
        self.company_ticket = company_ticker.upper()

        self.model = None

        self.data_to_fit = self.preprocessing(self.get_data_from_api(company_ticker, api_key))

        self._train_size = 972
        self._test_size = 90

        self.forecast = None

        self.best_prophet = None
        self.best_parameters = None
        self.learned_prophets = None

        self.SMAPE = None

        self.hyperparameters_dict: dict = {
            "seasonality_mode": ["additive", "multiplicative"],
            "n_changepoints": [i for i in range(300, 510, 50)],
            "changepoint_prior_scale": [i / 1000 for i in range(1, 501, 100)],
            "seasonality_prior_scale": [i / 100 for i in range(1, 1001, 200)],
            "holidays_prior_scale": [i / 100 for i in range(1, 1001, 200)],
            "changepoint_range": [i / 100 for i in range(80, 96, 5)],
            "growth": ["linear", "logistic"]
        }

    @staticmethod
    def get_data_from_api(company_ticker, api_key):
        """

        :param company_ticker:
        :param api_key:
        :return:
        """
        query = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}' \
                '&outputsize=full&apikey={}&datatype=csv'.format(company_ticker, api_key)
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
        self.model = OurProphet(**parameters)
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
        self.forecast = self.model.predict(future)

    @staticmethod
    def get_smape(y: np.array, y_pred: np.array):
        """
        Выдает значения метрики sMAPE
        :param y:
        :param y_pred:
        :return:
        """
        return np.mean(2 * abs(y - y_pred) / (y + y_pred)) * 100

    def _fit_predict_with_get_metrix_score_to_update_hyperparameters(self, item):
        """

        :param item:
        :return:
        """

        train_data = self.data_to_fit[self._test_size:self._test_size + self._train_size]
        test_data = self.data_to_fit[:self._test_size]

        cutoffs = pd.to_datetime(['2018-01-01', '2019-01-01', '2020-01-01'])
        prophet = OurProphet(**item)
        prophet.add_seasonality(name='monthly', period=21, fourier_order=3)
        prophet.add_seasonality('quarterly', period=63, fourier_order=8)
        prophet.add_country_holidays(country_name='US')
        prophet.fit(train_data)
        future = prophet.make_future_dataframe(self._test_size)
        forecast =prophet.predict(future)
        smape = self.get_smape(test_data.y, forecast.y)
        # df_cv = cross_validation(prophet, cutoffs=cutoffs, horizon='90 days')
        # df_p = performance_metrics(df_cv, rolling_window=1)
        return {"prophet": prophet, "metric": smape}

    def get_best_parameters(self):
        """

        :return:
        """
        all_parameters = [dict(zip(self.hyperparameters_dict.keys(), v)) for v in
                          itertools.product(*self.hyperparameters_dict.values())]
        smapes = []

        pool = mp.Pool()

        self.learned_prophets = pool.map(self._fit_predict_with_get_metrix_score_to_update_hyperparameters,
                                         all_parameters)

        self.best_prophet = self.learned_prophets[0].get("prophet")
        self.best_hyper_parameters = self.best_prophet.get_hyperparameters()
        # tuning_results = pd.DataFrame(all_parameters)
        # tuning_results['smapes'] = smapes
        # print(tuning_results)
        #
        # self.best_parameters = all_parameters[np.argmin(smapes)]
        # self.best_smape = min(smapes)
        # all_parameters.sorted
        # self.best_prophet
        # self.best_parameters =

    # @abstractmethod
    # def get_best_prediction(self):
    #     return
