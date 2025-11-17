from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import (
    product,
    productCategory,
    cookbook,
    ingredient,
    cookbookIngredient,
)
from .serializers import (
    productSerializer,
    productCategorySerializer,
    cookbookSerializer,
    ingredientSerializer,
    cookbookIngredientSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar productos del menú.
    Accesible por meseros para consultar productos.
    """
    # permission_classes = [IsMesero]
    
    queryset = product.objects.all()
    serializer_class = productSerializer

    @action(detail=False, methods=['get'])
    def get_all_products(self, request):
        """
        Obtener todos los productos disponibles en el menú.
        """
        all_products = product.objects.all()
        serializer = productSerializer(all_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def get_by_category(self, request):
        """
        Obtener productos filtrados por categoría.
        """
        category_id = request.query_params.get('categoryId')
        
        if not category_id:
            return Response(
                {'error': 'categoryId es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        products = product.objects.filter(categoryId=category_id)
        serializer = productSerializer(products, many=True)
        return Response(serializer.data)


class ProductAdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet para administración de productos del menú.
    Solo accesible por administradores.
    """
    # permission_classes = [IsAdmin]
    
    queryset = product.objects.all()
    serializer_class = productSerializer

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        """
        Agregar un nuevo producto al menú.
        """
        serializer = productSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        product_data = productSerializer(instance)
        return Response(product_data.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update_product(self, request, pk=None):
        """
        Actualizar un producto existente.
        """
        product_obj = self.get_object()
        serializer = productSerializer(product_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_product(self, request, pk=None):
        """
        Eliminar un producto del menú.
        """
        product_obj = self.get_object()
        product_obj.delete()
        return Response(
            {'message': 'Producto eliminado correctamente'}, 
            status=status.HTTP_204_NO_CONTENT
        )


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar categorías de productos.
    """
    queryset = productCategory.objects.all()
    serializer_class = productCategorySerializer

    @action(detail=False, methods=['post'])
    def add_category(self, request):
        serializer = productCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(productCategorySerializer(instance).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update_category(self, request, pk=None):
        category = self.get_object()
        serializer = productCategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_category(self, request, pk=None):
        category = self.get_object()
        category.delete()
        return Response({'message': 'Categoría eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)


class CookbookViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar recetas del libro de cocina.
    """
    queryset = cookbook.objects.all()
    serializer_class = cookbookSerializer

    @action(detail=True, methods=['get'])
    def get_ingredients(self, request, pk=None):
        """
        Obtener todos los ingredientes de una receta específica.
        """
        recipe = self.get_object()
        cookbook_ingredients = cookbookIngredient.objects.filter(recipe=recipe)
        serializer = cookbookIngredientSerializer(cookbook_ingredients, many=True)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar ingredientes.
    """
    queryset = ingredient.objects.all()
    serializer_class = ingredientSerializer

    @action(detail=False, methods=['post'])
    def add_ingredient(self, request):
        serializer = ingredientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(ingredientSerializer(instance).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update_ingredient(self, request, pk=None):
        ingredient_obj = self.get_object()
        serializer = ingredientSerializer(ingredient_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_ingredient(self, request, pk=None):
        ingredient_obj = self.get_object()
        ingredient_obj.delete()
        return Response({'message': 'Ingrediente eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


class CookbookIngredientViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar relaciones entre recetas e ingredientes.
    """
    queryset = cookbookIngredient.objects.all()
    serializer_class = cookbookIngredientSerializer

    @action(detail=False, methods=['post'])
    def add_cookbook_ingredient(self, request):
        serializer = cookbookIngredientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(cookbookIngredientSerializer(instance).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update_cookbook_ingredient(self, request, pk=None):
        obj = self.get_object()
        serializer = cookbookIngredientSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_cookbook_ingredient(self, request, pk=None):
        obj = self.get_object()
        obj.delete()
        return Response({'message': 'Relación eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)