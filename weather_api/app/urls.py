from django.urls import path
from .views import WeatherView, WeatherHistoryView

urlpatterns = [
    path('weather/', WeatherView.as_view(), name = 'weather'),
    path('weather/history', WeatherHistoryView.as_view(), name = 'weather-history'),
]