import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from models.our_prophet import OurProphet
import multiprocessing as mp


class StonksModel:
    def __init__(self, company_ticket: str, api_key: str = "ZRMG7N7CVNEFA2RY", model_type: str = "prophet"):

        self.api_key = api_key
        self.company_ticket = company_ticket.upper()

        # self._models = {"prophet": Prophet}

        self.model = None

        self._data_to_fit = None
        ##заданы на 3 года обучения и 1 год предсказания
        self._train_size = 756
        self._test_size = 252

        self.forecast = None
        self.forecast_period = None

        ##metrix
        self.rmse = None
        self.mape = None
        self.mae = None

        self._get_data()
        self._preprocessing()
        self._train_test_split()

    def _get_data(self):
        query = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey={}&datatype=csv'.format(
            self.company_ticket, self.api_key)
        self._data_to_fit = pd.read_csv(query)

    def _preprocessing(self):
        newDataFrame = pd.DataFrame(columns=["ds", "y"])
        newDataFrame.ds = pd.to_datetime(self._data_to_fit.timestamp)
        newDataFrame.y = self._data_to_fit.close
        self._data_to_fit = newDataFrame

    def _train_test_split(self):
        self._train_data = self._data_to_fit[self._test_size:self._test_size + self._train_size]
        self._test_data = self._data_to_fit[:self._test_size]

    ##TODO: учитывать праздники + доработать исполнение в режиме обучения
    def _generate_future_dates(self, days: int):
        future = self.model.make_future_dataframe(periods=days)
        future['day'] = future['ds'].dt.weekday
        future = future[future['day'] <= 4]
        future = future[future['ds'] >= self._test_data.loc[0, "ds"]]

        future = self.model.make_future_dataframe(periods=2 * days - future.shape[0])
        future['day'] = future['ds'].dt.weekday
        future = future[future['day'] <= 4]
        return future

    def fit(self, n_changepoints: int = None, changepoint_prior_scale: float = None, changepoint_range: float = None,
            fourier_order: int = None):
        """
        :param changepoint_prior_scale:
        :param changepoint_range:
        :param days_slice:
        :return:
        """
        self.model = OurProphet(daily_seasonality=True, n_changepoints=n_changepoints,
                                changepoint_prior_scale=changepoint_prior_scale,
                                changepoint_range=changepoint_range)
        self.model.add_seasonality(name='monthly', period=21, fourier_order=fourier_order)
        self.model.fit(self._train_data)

    ##TODO: поправить путаницу с размерностями обучения и теста
    def predict(self, days: int = 90):
        """
        :param date_period:
        :return:
        """
        future = self._generate_future_dates(days)
        self.forecast_period = future.shape[0]
        self.forecast = self.model.predict(future)

        self.mape = self._get_mape()
        self.mae = self._get_mae()
        self.rmse = self._get_rmse()

    def print_prophet_predict(self, add_changepoints: bool = False):
        """
        :param add_changepoints:
        :return:
        """
        fig = self.model.plot(self.forecast)
        # if add_changepoints:
        #     a = add_changepoints_to_plot(fig.gca(), self.model, self.forecast)

    def print_predict_with_real_data(self):
        """
        :param real_data:
        :param days_slice:
        :return:
        """
        forecast = self.forecast.merge(self._test_data, on="ds", how="left")
        plt.plot(forecast.ds, forecast.y, color="red")
        plt.plot(forecast.ds, forecast.yhat, color="black")
        plt.plot(forecast.ds, forecast.yhat_lower, color="blue")
        plt.plot(forecast.ds, forecast.yhat_upper, color="blue")
        plt.xticks(rotation=45, ha='right')
        plt.show()

    def _get_rmse(self):
        return np.sqrt(np.mean((self._test_data.y - self.forecast[-self.forecast_period:].yhat) ** 2))

    def _get_mape(self):
        return np.mean((self._test_data.y - self.forecast[-self.forecast_period:].yhat) / self._test_data.y) * 100

    def _get_mae(self):
        return np.mean(np.abs(self._test_data.y - self.forecast[-self.forecast_period:].yhat))

    def _get_metrix_sum(self):
        return self._get_mape() + self._get_rmse() + self._get_mae()

    def get_metrix(self):
        return "RMSE: " + str(self.rmse) + "\n" + "MAPE: " + str(self.mape) + "%" + "\n" + "MAE: " + str(self.mae)

    @staticmethod
    def _create_dict_of_hyperparameters_with_values():
        hyperparameters_combined = []
        hyperparameters_dict = {
            "n_changepoints": [i for i in range(0, 210, 10)],
            "changepoint_prior_scale": [i / 100 for i in range(0, 250, 50)],
            "changepoint_range": [i / 100 for i in range(0, 100, 5)],
        }
        for n_changepoints in hyperparameters_dict.get("n_changepoints"):
            for changepoint_prior_scale in hyperparameters_dict.get("changepoint_prior_scale"):
                for changepoint_range in hyperparameters_dict.get("changepoint_range"):
                    hyperparameters_combined.append({"n_changepoints": n_changepoints,
                                                     "changepoint_prior_scale": changepoint_prior_scale,
                                                     "changepoint_range": changepoint_range})
        return hyperparameters_combined

    def _fit_predict_with_get_metrix_score_to_update_hyperparameters(self, item):
        prophet = OurProphet(n_changepoints=item.get("n_changepoints"),
                             changepoint_prior_scale=item.get("changepoint_prior_scale"),
                             changepoint_range=item.get("changepoint_range"))
        prophet.add_seasonality(name='monthly', period=21, fourier_order=3)
        prophet.fit(self._train_data)
        future = prophet.make_future_dataframe(periods=self._test_size)
        future['day'] = future['ds'].dt.weekday
        future = future[future['day'] <= 4]
        future = future[future['ds'] >= self._test_data.loc[0, "ds"]]

        future = prophet.make_future_dataframe(periods=2 * self._test_size - future.shape[0])
        future['day'] = future['ds'].dt.weekday
        future = future[future['day'] <= 4]
        prophet.predict(future, self._test_data)
        return prophet

    def _update_hyperparameters(self):
        ##TODO: дополнить список гиперпараметров
        hyperparameters_combined = self._create_dict_of_hyperparameters_with_values()

        pool = mp.Pool()

        self.learned_prophets = pool.map(self._fit_predict_with_get_metrix_score_to_update_hyperparameters,
                                         hyperparameters_combined)

        self.learned_prophets.sort(key=lambda prophet: prophet.rmse)
        self.best_prophet = self.learned_prophets[0]
        self.best_hyperparameters = self.best_prophet.get_hyperparameters()

    def get_best_prediction(self):
        # self._train_test_split()
        self._update_hyperparameters()
        self.forecast = self.best_prophet._output_forecast
        self.print_predict_with_real_data()
        print(self.get_metrix())
