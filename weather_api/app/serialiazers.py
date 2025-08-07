from rest_framework import serializers
from .models import WeatherHistory

class WeatherHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherHistory
        fields = ['city', 'description', 'source', 'ip_address', "timestamp"]