from rest_framework import serializers
from .models import product

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ('id', 'name', 'price')

    def create(self, validated_data):
        return product.objects.create(**validated_data)