import requests
from decouple import config

API_KEY = config("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city):
    params = { "q": city,
    "appid": API_KEY,
    "units": "metric",
    "lang": "pt_br"
    }
    response = requests.get(BASE_URL, params = params)
    response.raise_for_status()
    return response.json()
