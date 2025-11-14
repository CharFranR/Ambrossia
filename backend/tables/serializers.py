from rest_framework import serializers
from .models import table, order, orderItem
from menu.models import product

class tableSerializer(serializers.ModelSerializer):
    class Meta:
        model = table
        fields = ['id', 'status','tableNumber']

    def create(self, validated_data):
        return table.objects.create(**validated_data)

class orderSerializer(serializers.ModelSerializer):
    tableId = serializers.PrimaryKeyRelatedField(queryset=table.objects.all(), required=False, allow_null=True)
    class Meta:
        model = order
        fields = ['id','tableId', 'status','createdAt', 'updatedAt', 'waiterId']

    def create(self, validated_data):
        return order.objects.create(**validated_data)
    
class orderItemSerializer(serializers.ModelSerializer):
    productId = serializers.PrimaryKeyRelatedField(queryset=product.objects.all())
    orderId = serializers.PrimaryKeyRelatedField(queryset=order.objects.all())

    class Meta:
        model = orderItem
        fields = ('id','orderId','productId','quantity','note')

    def create(self, validated_data):
        return orderItem.objects.create(**validated_data)