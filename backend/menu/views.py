from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Product, ProductCategory, CookBook
from .serializers import ProductSerializer, ProductCategorySerializer, CookBookSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar productos del menú.
    Accesible por meseros para consultar productos.
    """
    # permission_classes = [IsMesero]
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        """
        Crear un nuevo producto (también crea InventoryProduct).
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Actualizar un producto existente (actualiza InventoryProduct.lastUpdated).
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Pass request data through context for quantity updates
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=partial,
            context={'request_data': request.data}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_all_products(self, request):
        """
        Obtener todos los productos disponibles en el menú.
        """
        all_products = Product.objects.all()
        serializer = ProductSerializer(all_products, many=True)
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
        
        products = Product.objects.filter(categoryId=category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar categorías de productos.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class CookbookViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar recetas del libro de cocina.
    """
    queryset = CookBook.objects.all()
    serializer_class = CookBookSerializer