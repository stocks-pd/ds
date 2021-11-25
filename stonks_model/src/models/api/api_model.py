from stonks_model.src.models.stonksModel import StonksModel
import multiprocessing as mp


class ApiStonksModel(StonksModel):
    def __init__(self, estimator, api_key):
        StonksModel.__init__(self, estimator, api_key)
        self.param_grid = self.model.get_params_grid()

    def fit(self, parameters):
        StonksModel.fit(self, data=self.data_to_fit, parameters=parameters)

    def predict(self, periods: int = 90):
        StonksModel.predict(self, periods=periods)
        return self.forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_json()

    def get_best_parameters(self):
        best_params = {}
        pool = mp.Pool()

        return best_params
