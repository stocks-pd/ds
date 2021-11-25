from stonks_model.src.models.stonksModel import StonksModel


class ApiStonksModel(StonksModel):
    def fit(self, parameters):
        StonksModel.fit(self, data=self.data_to_fit, parameters=parameters)

    def predict(self, periods: int = 90):
        StonksModel.predict(self, periods=periods)
        return self.forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_json()
