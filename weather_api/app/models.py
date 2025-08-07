from django.db import models

# Create your models here.

class WeatherHistory(models.Model):
    city = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    source = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.city} - {self.description} - {self.timestamp}"