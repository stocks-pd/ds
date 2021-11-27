import itertools
from prophet import Prophet
from .interfaces.imodel import IModel
import pandas as pd


class OurProphet(Prophet, IModel):

    def get_hyperparameters(self):
        return {
            "growth": self.growth,
            "changepoints": self.changepoints,
            "n_changepoints": self.n_changepoints,
            "changepoint_range": self.changepoint_range,
            "yearly_seasonality": self.yearly_seasonality,
            "weekly_seasonality": self.weekly_seasonality,
            "daily_seasonality": self.daily_seasonality,
            "holidays": self.holidays,
            "seasonality_mode": self.seasonality_mode,
            "seasonality_prior_scale": self.seasonality_prior_scale,
            "holidays_prior_scale": self.holidays_prior_scale,
            "changepoint_prior_scale": self.changepoint_prior_scale,
            "mcmc_samples": self.mcmc_samples,
            "interval_width": self.interval_width,
            "uncertainty_samples": self.uncertainty_samples,
            "stan_backend": self.stan_backend
        }

    @staticmethod
    def get_params_grid(estimators_dict: dict, train_data: pd.DataFrame, test_data: pd.DataFrame) -> list:
        """

        :param estimators_dict:
        :param train_data:
        :type test_data: object
        """
        params = {
            "seasonality_mode": ["additive", "multiplicative"],
            "n_changepoints": [i for i in range(300, 510, 50)],
            "changepoint_prior_scale": [i / 1000 for i in range(1, 501, 100)],
            "seasonality_prior_scale": [i / 100 for i in range(1, 1001, 200)],
            "holidays_prior_scale": [i / 100 for i in range(1, 1001, 200)],
            "changepoint_range": [i / 100 for i in range(80, 96, 5)],
            "growth": ["linear", "logistic"],
            "estimator": estimators_dict,
            "train_data": train_data,
            "test_data": test_data
        }
        return [dict(zip(params.keys(), v)) for v in
                itertools.product(*params.values())]

    # TODO: учитывать праздники
    def make_future_dataframe(self, periods, freq='D', include_history=True):
        future = Prophet.make_future_dataframe(self, 2 * periods, freq=freq, include_history=False)
        future['day'] = future['ds'].dt.weekday
        future = future[future['day'] <= 4]
        future = future.iloc[:periods]
        return future
