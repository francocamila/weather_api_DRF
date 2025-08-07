from celery import shared_task
from .models import WeatherHistory

@shared_task
def save_weather_history(city, description, source, ip_address):
    WeatherHistory.objects.create(
        city=city,
        description=description,
        source=source,
        ip_address=ip_address
    )