from rest_framework import viewsets
from rest_framework.response import Response
from .models import product
from .serializers import productSerializer
from django.shortcuts import get_object_or_404
from users.permissions import IsMesero, IsAdmin
from rest_framework.decorators import action

class ProductViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsMesero]

    queryset = product.objects.all()
    serializer_class = productSerializer

    @action(detail=False, methods=['get'])
    def getAllProducts(self, request):
        allProducts = product.objects.all()
        serializer = productSerializer(allProducts, many=True)
        return Response(serializer.data)
        
class ProductAdminViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]

    queryset = product.objects.all()
    serializer_class = productSerializer

    @action(detail=False, methods=['post'])
    def addProduct(self, request):
        serializer = productSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        productData = productSerializer(instance)
        return Response (productData.data)

    @action(detail=False, methods=['put'])
    def updateProduct(self, request, id):
        product = get_object_or_404(product, pk=id)
        # Permitir actualización parcial de name y/o price
        data = {}
        if 'name' in request.data:
            data['name'] = request.data['name']
        if 'price' in request.data:
            data['price'] = request.data['price']
        serializer = productSerializer(product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)