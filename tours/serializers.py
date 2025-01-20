from rest_framework import serializers
from .models import Tour


class TourSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tour
    fields = ['id', 'title', 'description', 'price', 'image', 'status_promotion']