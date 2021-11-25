from stonks_model.src.models.baseStonksModel import BaseStonksModel
from matplotlib import pyplot as plt
import multiprocessing as mp
import itertools


class LearnStonksModel(BaseStonksModel):
    def __init__(self, estimator: str = "OurProphet", api_key: str = "ZRMG7N7CVNEFA2RY"):
        StonksModel.__init__(self, estimator, api_key)
        self.data_to_fit = self.preprocessing(self.get_data_from_api(company_ticker, api_key))
        self._train_test_split()

    def predict(self, periods: int = 90, freq="D", include_history=False):
        StonksModel.predict(self, periods, freq, include_history)

    def _train_test_split(self):
        self._train_data = self.data_to_fit[self._test_size:self._test_size + self._train_size]
        self._test_data = self.data_to_fit[:self._test_size]

    def get_best_prediction(self):
        self._train_test_split()
        self.get_best_parameters()
        # self.fit(self._train_data, **params)
        future = self.model.make_future_dataframe(self._test_data.shape[0], include_history=True)
        self.forecast = self.best_prophet.predict(future)
        self.SMAPE = self.get_smape(self._test_data.y.to_numpy(), self.forecast.yhat.to_numpy())
        self.print_all_timeline_predict_with_real_data()
        print(self.get_metrics())
        self.print_params(self.best_parameters)

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

    def print_params(self, prophet):
        print(*prophet.get_hyperparameters)

    def get_best_parameters(self):
        """

        :return:
        """
        all_parameters = [dict(zip(self.hyperparameters_dict.keys(), v)) for v in
                          itertools.product(*self.hyperparameters_dict.values())]

        pool = mp.Pool()

        self.learned_prophets = pool.map(self._fit_predict_with_get_metrix_score_to_update_hyperparameters,
                                         all_parameters)

        self.best_prophet = self.learned_prophets[0].get("prophet")
        self.best_hyper_parameters = self.best_prophet.get_hyperparameters()
