from rest_framework import serializers
from .models import Item


class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("year", "transmision", "km",
                  "title", "marca", "discount_price", "price", "image", "get_absolute_url")
