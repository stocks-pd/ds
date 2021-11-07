import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot


class StonksPrediction:
    def __init__(self, company_ticket: str, api_key: str = "ZRMG7N7CVNEFA2RY", data_to_fit=None):
        self.prophet = None
        self.changepoint_range = None
        self._data_to_fit = data_to_fit
        self.company_ticket = company_ticket
        self.api_key = api_key
        self.forecast = None
        self.forecast_period = None
        self.rmse = None
        self.mape = None
        self.mae = None
        self._get_data()
        self._preprocessing()

    def _get_data(self):
        query = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey={}&datatype=csv'.format(
            self.company_ticket, self.api_key)
        self._data_to_fit = pd.read_csv(query)

    def _preprocessing(self):
        newDataFrame = pd.DataFrame(columns=["ds", "y"])
        newDataFrame.ds = pd.to_datetime(self._data_to_fit.timestamp)
        newDataFrame.y = self._data_to_fit.close
        self._data_to_fit = newDataFrame

    def fit(self, changepoint_prior_scale: float = None, changepoint_range: float = None, train_test_plit: int = 0):
        """

        :param changepoint_prior_scale:
        :param changepoint_range:
        :param days_slice:
        :return:
        """
        self._train_data = self._data_to_fit[train_test_plit:]
        self._test_data = self._data_to_fit[:train_test_plit]
        self.prophet = Prophet(daily_seasonality=True, changepoint_prior_scale=changepoint_prior_scale,
                               changepoint_range=changepoint_range)
        self.prophet.fit(self._train_data)

    def predict(self, date_period: int = 90):
        """

        :param date_period:
        :return:
        """
        ##TODO: сделать адекватный просчет горизонта прогноза и фильтрации дат от пропусков в данных для обучения
        future = self.prophet.make_future_dataframe(periods=2 * date_period)
        future['day'] = future['ds'].dt.weekday
        future = future[future['day'] <= 4]
        self.forecast_period = future.shape[0]
        self.forecast = self.prophet.predict(future)

    def print_prophet_predict(self, add_changepoints: bool = False):
        """

        :param add_changepoints:
        :return:
        """
        fig = self.prophet.plot(self.forecast)
        if add_changepoints:
            a = add_changepoints_to_plot(fig.gca(), self.prophet, self.forecast)

    def print_predict_with_real_data(self):
        """

        :param real_data:
        :param days_slice:
        :return:
        """
        forecast = self.forecast[-self.forecast_period:].merge(self._test_data, on="ds", how="right")
        plt.plot(forecast.ds, forecast.y, color="red")
        plt.plot(forecast.ds, forecast.yhat, color="black")
        plt.plot(forecast.ds, forecast.yhat_lower, color="blue")
        plt.plot(forecast.ds, forecast.yhat_upper, color="blue")
        plt.xticks(rotation=45, ha='right')
        plt.show()

    ##TODO: убрать костыль с начальной датой отсчет времени
    def _get_rmse(self):
        self.rmse = np.sqrt(np.mean((self._test_data.y - self.forecast[-self.forecast_period:self.forecast_period -
                                                                                             self._test_data.shape[
                                                                                                 0]].yhat) ** 2))

    def _get_mape(self):
        self.mape = np.mean((self._test_data.y - self.forecast[-self.forecast_period:self.forecast_period -
                                                                                     self._test_data.shape[
                                                                                         0]].yhat) / self._test_data.y) * 100

    def _get_mae(self):
        self.mae = np.mean(np.abs(self._test_data.y - self.forecast[-self.forecast_period:self.forecast_period -
                                                                                     self._test_data.shape[
                                                                                         0]].yhat))

    def get_metrix(self):
        self._get_rmse()
        self._get_mape()
        self._get_mae()
        return "RMSE: " + str(self.rmse) + "\n" + "MAPE: " + str(self.mape) + "\n" + "MAE: " + str(self.mae)
