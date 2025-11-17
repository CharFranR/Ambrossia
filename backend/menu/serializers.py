from rest_framework import serializers
from .models import product, productCategory, cookbook, ingredient, cookbookIngredient


class productCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = productCategory
        fields = ("id", "name")

    def create(self, validated_data):
        return productCategory.objects.create(**validated_data)


class productSerializer(serializers.ModelSerializer):
   
    categoryId = serializers.PrimaryKeyRelatedField(queryset=productCategory.objects.all())

    class Meta:
        model = product
        fields = ("id", "name", "price", "categoryId")

    def create(self, validated_data):
        return product.objects.create(**validated_data)

class cookbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = cookbook
        fields = ("id", "name", "note")

    def create(self, validated_data):
        return cookbook.objects.create(**validated_data)

class ingredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingredient
        fields = ("id", "name", "unit")

    def create(self, validated_data):
        return ingredient.objects.create(**validated_data)

class cookbookIngredientSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=cookbook.objects.all())
    ingredient = serializers.PrimaryKeyRelatedField(queryset=ingredient.objects.all())

    class Meta:
        model = cookbookIngredient
        fields = ("id", "recipe", "ingredient")

    def create(self, validated_data):
        return cookbookIngredient.objects.create(**validated_data)