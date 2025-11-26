from rest_framework import serializers
from django.utils import timezone
from .models import Product, ProductCategory, CookBook, InventoryProduct


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("id", "name")

    def create(self, validated_data):
        return ProductCategory.objects.create(**validated_data)


class CookBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookBook
        fields = ("id", "name", "note", "preparation_time", "servings", "instructions", "is_active", "version", "image")

    def create(self, validated_data):
        return CookBook.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    categoryId = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())
    cookbookId = serializers.PrimaryKeyRelatedField(queryset=CookBook.objects.all())

    class Meta:
        model = Product
        fields = ("id", "name", "price", "cookbookId", "categoryId")

    def create(self, validated_data):
        # Create the product
        new_product = Product.objects.create(**validated_data)
        
        # Create corresponding InventoryProduct with initial quantity=0
        InventoryProduct.objects.create(
            productId=new_product,
            quantity=0
        )
        
        return new_product
    
    def update(self, instance, validated_data):
        # Update the product fields
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.cookbookId = validated_data.get('cookbookId', instance.cookbookId)
        instance.categoryId = validated_data.get('categoryId', instance.categoryId)
        instance.save()
        
        # Update inventory product if quantity is provided
        if 'quantity' in self.context.get('request_data', {}):
            inventory_product = InventoryProduct.objects.filter(productId=instance).first()
            if inventory_product:
                inventory_product.quantity = self.context['request_data']['quantity']
                inventory_product.save()  # This will auto-update lastUpdated
        
        return instance