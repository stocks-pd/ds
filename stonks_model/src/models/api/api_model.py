from stonks_model.src.models.baseStonksModel import BaseStonksModel



class ApiBaseStonksModel(BaseStonksModel):
    def __init__(self, estimator: str = "OurProphet", api_key: str = "ZRMG7N7CVNEFA2RY"):
        BaseStonksModel.__init__(self, estimator, api_key)
        self.param_grid = self.model.get_params_grid()

    def predict(self, periods: int = 90):
        BaseStonksModel.predict(self, periods=periods)
        return self.forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_json()


