from rest_framework import serializers
from .models import Tour, Driver, TourSchedule, TourImage


class TourImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = TourImage
    fields = ['image']

class TourSerializer(serializers.ModelSerializer):
  images = TourImageSerializer(many=True, read_only=True)
  image_url = serializers.SerializerMethodField()

  class Meta:
    model = Tour
    fields = '__all__'
    extra_fields = ['images', 'image_url']

  def get_image_url(self, obj):
    return obj.image.url if obj.image else None

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