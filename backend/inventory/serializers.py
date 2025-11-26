from rest_framework import serializers
from django.utils import timezone
from django.db import models
from .models import (
    inventoryProduct,
    inventoryProductType,
    inventoryMovementType,
    inventoryMovement,
)

# Serializer de tipos 
class InventoryProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = inventoryProductType
        fields = ("id", "name")

    def create(self, validated_data):
        return inventoryProductType.objects.create(**validated_data)

class InventoryMovementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = inventoryMovementType
        fields = ("id", "name")

    def create(self, validated_data):
        return inventoryMovementType.objects.create(**validated_data)

# Serializer de modelos
class InventoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = inventoryProduct
        fields = ("id", "name", "quantity","type", "lastUpdated")

    def create(self, validated_data):
        user_id = self.context.get('userId') or 1
        product_type = inventoryProductType.objects.get(name = validated_data['type'])

        # Creamos el producto
        new_product = inventoryProduct.objects.create()
        new_product.name = validated_data['name']
        new_product.type = product_type
        new_product.quantity = validated_data['quantity']

        # Guardamos el movimiento
        new_movement = inventoryMovement.objects.create()
        new_movement.itemId = new_product
        new_movement.movementType,_ = inventoryMovementType.objects.get_or_create(name="add")
        new_movement.userId = user_id

        return new_product
    
    def destoy(self, validated_data):
        product_id = validated_data['product_id']
        user_id = self.context.get('userId') or 1
        
        # Eliminamos el producto
        deleted_product = inventoryProduct.objects.get(id=product_id)
        deleted_product.delete()

        # Guardamos el movimient0
        new_movement = inventoryMovement.objects.create()
        new_movement.itemId = product_id
        new_movement.userId = user_id

        return ("Delete successful")

    def update(self, instance, validated_data):
        product_id = validated_data['product_id']
        user_id = self.context.get('userId') or 1

        # Actualizamos el producto
        updated_product = inventoryProduct.objects.get(id = product_id)
        updated_product.name = validated_data['name']
        updated_product.quantity = validated_data['quantity']
        updated_product.type = validated_data['type']
        updated_product.save()

         # Guardamos el movimient0
        new_movement = inventoryMovement.objects.create()
        new_movement.itemId = product_id
        new_movement.movementType,_ = inventoryMovementType.objects.get_or_create(name="update")
        new_movement.userId = user_id
        
        return super().update(instance, validated_data)
        


class InventoryMovementSerializer(serializers.ModelSerializer):
    itemType = serializers.PrimaryKeyRelatedField(queryset=inventoryProductType.objects.all())
    itemId = serializers.PrimaryKeyRelatedField(queryset=inventoryProduct.objects.all())
    movementType = serializers.PrimaryKeyRelatedField(queryset=inventoryMovementType.objects.all())

    class Meta:
        model = inventoryMovement
        fields = ("id", "itemType", "itemId", "movementType", "createdAt")

    def create(self, validated_data):
        return inventoryMovement.objects.create(**validated_data)