from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from decouple import config
import requests
import unicodedata
from .utils import fetch_weather
from .tasks import save_weather_history
from .serialiazers import WeatherHistorySerializer
from .models import WeatherHistory
from drf_spectacular.utils import extend_schema, OpenApiParameter
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def get_client_ip(request):
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                ip = x_forwarded_for.split(",")[0]
            else:
                ip = request.META.get("REMOTE_ADDR")
            return ip

def slugify_key(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text.lower().replace(" ", "_")

def create_log(city, source, ip):
     logger.info("Weather data returned", extra={
            "city": city,
            "source": source,
            "ip": ip,
        })

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='city',
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description='Name of the city',
        ),
    ]
)


class WeatherView(APIView):

    def get(self, request):
        city = request.query_params.get("city")
        if not city: 
            return Response({"error": "Parâmetro cidade é obrigatório!"}, status = status.HTTP_400_BAD_REQUEST)
        
        key = f"weather:{slugify_key(city)}"
        cached_data = cache.get(key)
        print(cached_data)
        ip = get_client_ip(request)

        if cached_data:
            source = "cache"
            create_log(city, source, ip)
            save_weather_history.delay(city, cached_data['weather'][0]['description'], source, ip)
            return Response({"source": source, "data": cached_data['weather'][0]['description']})
        
        try:
            data = fetch_weather(city)
            cache.set(key, data, timeout= config('CACHE_TIMEOUT'))
            source = "api"
            create_log(city, source, ip)
            save_weather_history.delay(city, data['weather'][0]['description'], source, ip)
            return Response ({"source": source, "data": data['weather'][0]['description']})
        except requests.RequestException as e:
            logger.exception("Unexpected error fetching weather data", extra={
                "error": str(e),
            })
            return Response({"error": str(e)}, status = status.HTTP_502_BAD_GATEWAY)
        
class WeatherHistoryView(APIView):
    def get(self, request):
        ip = get_client_ip(request)
        queryset = WeatherHistory.objects.filter(ip_address = ip).order_by('-timestamp')[:10]
        serializer = WeatherHistorySerializer(queryset, many = True)
        return Response(serializer.data)