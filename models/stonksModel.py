import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot


class StonksModel:
    def __init__(self, company_ticket: str, api_key: str = "ZRMG7N7CVNEFA2RY", model_type: str = "prophet",
                 train_test_split_scale: float = 0.8):

        self.train_test_split_scale = train_test_split_scale
        self.api_key = api_key
        self.company_ticket = company_ticket.upper()

        # self._models = {"prophet": Prophet}

        self.model = None

        self._data_to_fit = None

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
        split_index = int(self._data_to_fit.shape[0] * (1 - self.train_test_split_scale))
        self._train_data = self._data_to_fit[split_index:]
        self._test_data = self._data_to_fit[:split_index]
        self.forecast_period = self._test_data.shape[0]

    ##TODO: добавить просчет праздников
    def _generate_future_dates(self, days: int):
        future = self.model.make_future_dataframe(periods=days)
        future['day'] = future['ds'].dt.weekday
        future = future[future['day'] <= 4]
        future = future[future['ds'] >= self._test_data.loc[0, "ds"]]
        future = self.model.make_future_dataframe(periods=2 * days - future.shape[0])
        future['day'] = future['ds'].dt.weekday
        future = future[future['day'] <= 4]
        return future

    def fit(self, n_changepoints: int = None, changepoint_prior_scale: float = None, changepoint_range: float = None):
        """
        :param changepoint_prior_scale:
        :param changepoint_range:
        :param days_slice:
        :return:
        """
        self.model = Prophet(daily_seasonality=True, n_changepoints=n_changepoints,
                             changepoint_prior_scale=changepoint_prior_scale,
                             changepoint_range=changepoint_range)
        self.model.fit(self._train_data)

    def predict(self, days: int = None):
        """
        :param date_period:
        :return:
        """

        if days is None:
            future = self._generate_future_dates(self.forecast_period)
        else:
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
        if add_changepoints:
            a = add_changepoints_to_plot(fig.gca(), self.model, self.forecast)

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
        return np.sqrt(np.mean((self._test_data.y - self.forecast[-self.forecast_period:].yhat) ** 2))

    def _get_mape(self):
        return np.mean((self._test_data.y - self.forecast[-self.forecast_period:].yhat) / self._test_data.y) * 100

    def _get_mae(self):
        return np.mean(np.abs(self._test_data.y - self.forecast[-self.forecast_period:].yhat))

    def _get_metrix_sum(self):
        return self._get_mape() + self._get_rmse() + self._get_mae()

    def get_metrix(self):
        return "RMSE: " + str(self.rmse) + "\n" + "MAPE: " + str(self.mape) + "\n" + "MAE: " + str(self.mae)

    def _update_hyperparameters(self):
        ##TODO: дополнить список гиперпараметров и подумать об оптимизации процесса перебора
        sum_of_metrixes_list = []
        hyperparameters_dict = {
            "n_changepoints": [i for i in range(100, 120, 50)],
            "changepoint_prior_scale": [i / 100 for i in range(10, 20, 50)],
            "changepoint_range": [i / 100 for i in range(10, 20, 50)],
        }
        iter = 1
        for n_changepoints in hyperparameters_dict.get("n_changepoints"):
            for changepoint_prior_scale in hyperparameters_dict.get("changepoint_prior_scale"):
                for changepoint_range in hyperparameters_dict.get("changepoint_range"):
                    print(iter)
                    self.fit(n_changepoints, changepoint_prior_scale, changepoint_range)
                    self.predict()
                    sum_of_metrixes_list.append({
                        "metrix_sum": self._get_metrix_sum(),
                        "hyperparameters": {
                            "n_changepoints": n_changepoints,
                            "changepoint_prior_scale": changepoint_prior_scale,
                            "changepoint_range": changepoint_range
                        }
                    })
                    iter += 1
        sum_of_metrixes_list.sort(key=lambda metrix: metrix.get("metrix_sum"))
        self.best_hyperparameters = sum_of_metrixes_list[0].get("hyperparameters")
        self._hyperparameters_with_metrix = sum_of_metrixes_list

    def get_best_prediction(self):
        self._update_hyperparameters()
        self.fit(self.best_hyperparameters.get("n_changepoints"),
                 self.best_hyperparameters.get("changepoint_prior_scale"),
                 self.best_hyperparameters.get("changepoint_range"))
        self.predict()
        self.print_predict_with_real_data()
        print(self.get_metrix())