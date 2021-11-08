import numpy as np
import pandas as pd
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot


class OurProphet(Prophet):
    def __init__(self,
                 growth='linear',
                 changepoints=None,
                 n_changepoints=25,
                 changepoint_range=0.8,
                 yearly_seasonality='auto',
                 weekly_seasonality='auto',
                 daily_seasonality='auto',
                 holidays=None,
                 seasonality_mode='additive',
                 seasonality_prior_scale=10.0,
                 holidays_prior_scale=10.0,
                 changepoint_prior_scale=0.05,
                 mcmc_samples=0,
                 interval_width=0.80,
                 uncertainty_samples=1000,
                 stan_backend=None):
        Prophet.__init__(self,
                         growth,
                         changepoints,
                         n_changepoints,
                         changepoint_range,
                         yearly_seasonality,
                         weekly_seasonality,
                         daily_seasonality,
                         holidays,
                         seasonality_mode,
                         seasonality_prior_scale,
                         holidays_prior_scale,
                         changepoint_prior_scale,
                         mcmc_samples,
                         interval_width,
                         uncertainty_samples,
                         stan_backend)
        self.rmse = None
        self._output_forecast = None

    def predict(self, df=None, real_data: pd.DataFrame = None):
        self._output_forecast = Prophet.predict(self, df)
        if real_data is not None:
            self.rmse = self._get_rmse(real_data)
        return self._output_forecast

    def _get_rmse(self, real_data):
        return np.sqrt(np.mean((real_data.y - self._output_forecast[-real_data.shape[0]:].yhat) ** 2))

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
