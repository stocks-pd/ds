from django.urls import path, include
from . import views

app_name = 'stonks_model_app'
urlpatterns = [
    path('predict/<str:tiker>&<int:periods>', views.predict, name='predict'),
    path('fit', views.fit, name='predict'),
    # path('update_recommendations', views.update_recommendations, name='update_recommendations'),
    path('update_parameters', views.update_parameters, name='update_parameters'),
]
