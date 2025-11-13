from rest_framework import serializers
from django.utils import timezone
from .models import (
    inventoryProduct,
    inventoryIngredient,
    inventoryItemType,
    inventoryMovementType,
    inventoryMovement,
)


class InventoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = inventoryProduct
        fields = ("id", "productId", "quantity", "lastUpdated")

    def create(self, validated_data):
        return inventoryProduct.objects.create(**validated_data)

class InventoryIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = inventoryIngredient
        fields = ("id", "ingredientId", "quantity", "lastUpdated")
        
    def create(self, validated_data):
        return inventoryIngredient.objects.create(**validated_data)

class InventoryItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = inventoryItemType
        fields = ("id", "name")

    def create(self, validated_data):
        return inventoryItemType.objects.create(**validated_data)

class InventoryMovementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = inventoryMovementType
        fields = ("id", "name")

    def create(self, validated_data):
        return inventoryMovementType.objects.create(**validated_data)


class InventoryMovementSerializer(serializers.ModelSerializer):
    itemType = serializers.PrimaryKeyRelatedField(queryset=inventoryItemType.objects.all())
    itemId = serializers.PrimaryKeyRelatedField(queryset=inventoryProduct.objects.all())
    movementType = serializers.PrimaryKeyRelatedField(queryset=inventoryMovementType.objects.all())

    class Meta:
        model = inventoryMovement
        fields = ("id", "itemType", "itemId", "movementType", "createdAt")

    def create(self, validated_data):
        return inventoryMovement.objects.create(**validated_data)