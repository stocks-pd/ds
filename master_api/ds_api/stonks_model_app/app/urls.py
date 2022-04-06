from django.urls import path, include
from . import views

app_name = 'stonks_model_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:ticker>', views.detail, name='detail'),
    path('predict', views.predict, name='predict'),
    path('fit', views.fit, name='predict'),
    path('test_predict/<str:ticker>', views.test_predict, name='test_predict'),
    # path('update_recommendations', views.update_recommendations, name='update_recommendations'),
    path('update_parameters', views.update_parameters, name='update_parameters'),
]
