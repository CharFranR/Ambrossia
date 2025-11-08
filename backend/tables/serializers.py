from rest_framework import serializers
from .models import table, order
from bill.models import bill
from menu.models import product

class tableSerializer(serializers.ModelSerializer):
    class Meta:
        model = table
        fields = ['id', 'status']

    def create(self, validated_data):
        return table.objects.create(**validated_data)

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ['id', 'name', 'price']

    def create(self, validated_data):
        return product.objects.create(**validated_data)

class orderSerializer(serializers.ModelSerializer):
    table = serializers.PrimaryKeyRelatedField(queryset=table.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=product.objects.all())
    class Meta:
        model = order
        fields = ['id','table', 'product', 'status','createdAt', 'closedAt', 'note']

    def create(self, validated_data):
        return order.objects.create(**validated_data)