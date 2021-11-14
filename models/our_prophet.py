import numpy as np
import pandas as pd
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot


class OurProphet(Prophet):

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

    # TODO: учитывать праздники
    def make_future_dataframe(self, periods, freq='D', include_history=True):
        future = Prophet.make_future_dataframe(self, 2 * periods, freq=freq, include_history=False)
        future['day'] = future['ds'].dt.weekday
        future = future[future['day'] <= 4]
        future = future.iloc[:periods]
        return future
