from models.stonksModel import StonksModel
from matplotlib import pyplot as plt

class LearnStonksModel(StonksModel):
    def __init__(self, company_ticket: str, api_key: str = "ZRMG7N7CVNEFA2RY"):
        StonksModel.__init__(self, company_ticket, api_key)
        self._train_test_split()

    def predict(self, periods: int = 90, freq="D", include_history=False):
        StonksModel.predict(periods, freq, include_history)


    def _train_test_split(self):
        self._train_data = self.data_to_fit[self._test_size:self._test_size + self._train_size]
        self._test_data = self.data_to_fit[:self._test_size]

    def get_best_prediction(self):
        self._train_test_split()
        self.get_best_hyperparameter_and_prophet()
        self.forecast = self.best_prophet._output_forecast
        self.print_predict_with_real_data()
        print(self.get_metrix())

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

    def get_metrix(self):
        return "RMSE: " + str(self.rmse) + "\n" + "MAPE: " + str(self.mape) + "%" + "\n" + "MAE: " + str(self.mae)