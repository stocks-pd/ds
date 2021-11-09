from models.stonksModel import StonksModel
from matplotlib import pyplot as plt


class LearnStonksModel(StonksModel):
    def __init__(self, company_ticket: str, api_key: str = "ZRMG7N7CVNEFA2RY"):
        StonksModel.__init__(self, company_ticket, api_key)
        self._train_test_split()

    def predict(self, periods: int = 90, freq="D", include_history=False):
        StonksModel.predict(self, periods, freq, include_history)

    def _train_test_split(self):
        self._train_data = self.data_to_fit[self._test_size:self._test_size + self._train_size]
        self._test_data = self.data_to_fit[:self._test_size]

    def get_best_prediction(self):
        self._train_test_split()
        self.get_best_hyperparameter_and_prophet(True)
        future = self.model.make_future_dataframe(self._test_data.shape[0], include_history=True)
        self.forecast = self.best_prophet.predict(future)
        self.SMAPE = self.get_smape(self._test_data.y.to_numpy(), self.forecast.yhat.to_numpy())
        self.print_all_timeline_predict_with_real_data()
        print(self.get_metrics())

    def print_predict_with_real_data(self):
        forecast = self.forecast.merge(self._test_data, on="ds", how="left")

        plt.plot(forecast.ds, forecast.y, color="red")
        plt.plot(forecast.ds, forecast.yhat, color="black")
        plt.plot(forecast.ds, forecast.yhat_lower, linestyle='--',
                 linewidth=2,
                 color='darkmagenta')
        plt.plot(forecast.ds, forecast.yhat_upper, linestyle='--',
                 linewidth=2,
                 color='darkmagenta')
        plt.title(self.company_ticket)
        plt.xlabel("Дата")
        plt.ylabel("Цена")
        plt.xticks(rotation=45, ha='right')
        plt.show()

    def print_all_timeline_predict_with_real_data(self):
        forecast = self.forecast.merge(self.data_to_fit[:324], on="ds", how="right")
        plt.figure(figsize=(18, 10))
        plt.plot(forecast.ds, forecast.y, color="red")
        plt.plot(forecast.ds, forecast.yhat, color="black")
        plt.plot(forecast.ds, forecast.yhat_lower, linestyle='--',
                 linewidth=2,
                 color='darkmagenta')
        plt.plot(forecast.ds, forecast.yhat_upper, linestyle='--',
                 linewidth=2,
                 color='darkmagenta')
        plt.title(self.company_ticket)
        plt.xlabel("Дата")
        plt.ylabel("Цена")
        plt.xticks(rotation=45, ha='right')
        plt.show()

    def get_metrics(self):
        return "sMAPE: " + str(round(self.SMAPE)) + "%"
