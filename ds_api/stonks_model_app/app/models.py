from django.db import models
from django.utils import timezone


# Create your models here.
class ProphetParams(models.Model):
    find_date = models.DateTimeField("Дата подбора параметров", default=timezone.now())
    growth = models.CharField("Параметр growth", max_length=10, default='linear')
    # changepoints = models.Ar
    n_changepoints = models.IntegerField("Параметр n_changepoints", default=25)
    changepoint_range = models.FloatField("Параметр changepoint_range", default=0.8)
    yearly_seasonality = models.CharField("Параметр yearly_seasonality", max_length=200, default='auto')
    weekly_seasonality = models.CharField("Параметр weekly_seasonality", max_length=200, default='auto')
    daily_seasonality = models.CharField("Параметр daily_seasonality", max_length=200, default='auto')
    # holidays =
    seasonality_mode = models.CharField("Параметр seasonality_mode", max_length=20, default='additive')
    seasonality_prior_scale = models.FloatField("Параметр seasonality_prior_scale", default=10.0)
    holidays_prior_scale = models.FloatField("Параметр holidays_prior_scale", default=10.0)
    changepoint_prior_scale = models.FloatField("Параметр changepoint_prior_scale", default=0.05)
    mcmc_samples = models.IntegerField("Параметр mcmc_samples", default=0)
    interval_width = models.FloatField("Параметр interval_width", default=0.80)
    uncertainty_samples = models.IntegerField("Параметр uncertainty_samples", default=1000)
    # stan_backend = models.CharField("Параметр stan_backend", max_length=200, null=True, default=None)
    score = models.FloatField("Оценка модели с такими параметрами", null=True)

    def __str__(self):
        return str(self.find_date) + str(self.score)

    def get_params(self):
        return {
            "growth": self.growth,
            # "changepoints": self.changepoints,
            "n_changepoints": self.n_changepoints,
            "changepoint_range": self.changepoint_range,
            "yearly_seasonality": self.yearly_seasonality,
            "weekly_seasonality": self.weekly_seasonality,
            "daily_seasonality": self.daily_seasonality,
            # "holidays": self.holidays,
            "seasonality_mode": self.seasonality_mode,
            "seasonality_prior_scale": self.seasonality_prior_scale,
            "holidays_prior_scale": self.holidays_prior_scale,
            "changepoint_prior_scale": self.changepoint_prior_scale,
            "mcmc_samples": self.mcmc_samples,
            # "interval_width": self.interval_width,
            "uncertainty_samples": self.uncertainty_samples,
            # "stan_backend": self.stan_backend
        }
#
#
# class Recommendations(models.Model):
#     date_of_recommendation = models.DateTimeField("Дата подборки", default=timezone.now())
#     tiker = models.CharField("Тикер", max_length=10)
#     period = models.CharField("Период прогноза", max_length=10)
#     price = models.FloatField("Прогнозная цена")
#     risk = models.FloatField("Риск")
