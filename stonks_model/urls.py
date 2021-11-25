from django.urls import path

from . import views

app_name = 'stonks_model'
urlpatterns = [
    path('predict/<str:tiker>&<int:periods>', views.predict, name='predict'),
    path('fit', views.fit, name='predict'),

]
