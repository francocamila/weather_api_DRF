#Integration tests
import pytest
from rest_framework.test import APIClient
from django.core.cache import cache
import unicodedata


@pytest.mark.django_db
def test_weather_view_no_cache(monkeypatch):
    client = APIClient()

    def mock_fetch_weather(city):
        return {'coord': {'lon': -47.9297, 'lat': -15.7797}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'céu limpo', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 16.51, 'feels_like': 15.97, 'temp_min': 16.51, 'temp_max': 16.51, 'pressure': 1017, 'humidity': 67, 'sea_level': 1017, 'grnd_level': 890}, 'visibility': 10000, 'wind': {'speed': 1.54, 'deg': 280}, 'clouds': {'all': 0}, 'dt': 1754545286, 'sys': {'type': 1, 'id': 8336, 'country': 'BR', 'sunrise': 1754559173, 'sunset': 1754600525}, 'timezone': -10800, 'id': 3469058, 'name': 'Brasília', 'cod': 200}
    
    monkeypatch.setattr("app.views.fetch_weather", mock_fetch_weather)

    response = client.get("/api/weather/?city=Brasília")
    assert response.status_code == 200
    assert response.data["source"] == "api"
    assert "data" in response.data

@pytest.mark.django_db
def test_weather_view_with_cache():
    client = APIClient()
    city = "São Paulo"
    city = unicodedata.normalize('NFKD', city).encode('ascii', 'ignore').decode('ascii')
    city = city.lower().replace(" ", "_")
    key = f"weather:{city}"
    cached_data = {'coord': {'lon': -46.6361, 'lat': -23.5475}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'nublado', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 14.67, 'feels_like': 14.59, 'temp_min': 13.94, 'temp_max': 15.81, 'pressure': 1022, 'humidity': 92, 'sea_level': 1022, 'grnd_level': 930}, 'visibility': 10000, 'wind': {'speed': 2.68, 'deg': 91, 'gust': 3.13}, 'clouds': {'all': 100}, 'dt': 1754544584, 'sys': {'type': 2, 'id': 2082654, 'country': 'BR', 'sunrise': 1754559472, 'sunset': 1754599606}, 'timezone': -10800, 'id': 3448439, 'name': 'São Paulo', 'cod': 200}
    cache.set(key, cached_data)
    response = client.get(f"/api/weather/?city={city}")
    assert response.status_code == 200
    assert response.data["source"] == "cache"
    assert response.data["data"] == cached_data['weather'][0]['description']
