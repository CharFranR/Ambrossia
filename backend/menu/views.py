from rest_framework import viewsets
from rest_framework.response import Response
from .models import product, productCategory
from .serializers import productSerializer, productCategorySerializer
from django.shortcuts import get_object_or_404
from users.permissions import IsMesero, IsAdmin
from rest_framework.decorators import action

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product operations.
    Provides CRUD operations and custom actions.
    """
    # permission_classes = [IsMesero]

    queryset = product.objects.all()
    serializer_class = productSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new product. Requires name, price, and categoryId.
        """
        # Ensure categoryId is provided, create default if missing
        if 'categoryId' not in request.data:
            # Create or get a default category
            default_category, _ = productCategory.objects.get_or_create(
                name='General',
                defaults={'name': 'General'}
            )
            data = request.data.copy()
            data['categoryId'] = default_category.id
        else:
            data = request.data
            
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update a product. Allows partial updates of name, price, and categoryId.
        """
        partial = kwargs.pop('partial', True)  # Allow partial updates by default
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product category operations.
    """
    queryset = productCategory.objects.all()
    serializer_class = productCategorySerializer