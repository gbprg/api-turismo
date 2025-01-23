from rest_framework import serializers
from .models import Tour, Driver, TourSchedule


class TourSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tour
    fields = ['id', 'title', 'description', 'price', 'image', 'status_promotion']

    def get_image(self, obj):
      return obj.image.url if obj.image else '/path/to/default/image.jpg'

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
      model = Driver
      fields = ['id', 'name', 'vehicle']  # Apenas informações públicas do motorista

class TourScheduleSerializer(serializers.ModelSerializer):
    tour = TourSerializer(read_only=True)  # Inclui os detalhes do tour
    driver = DriverSerializer(read_only=True)  # Inclui os detalhes do motorista
    
    class Meta:
      model = TourSchedule
      fields = [
        'id',
        'tour',
        'driver',
        'date',
        'time',
        'available_seats',
      ]