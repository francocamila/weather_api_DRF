from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import fetch_weather
# Create your views here.

class WeatherView(APIView):
    def get(self, request):
        city = request.query_params.get("city")
        if not city: 
            return Response({"error": "Parâmetro cidade é obrigatório!"}, status = status.HTTP_400_BAD_REQUEST)
        try:
            data = fetch_weather(city)
            return Response ({"source": "api", "data": data})
        except requests.RequestException as e:
            return Response({"error": str(e)}, status = status.HTTP_502_BAD_GATEWAY)