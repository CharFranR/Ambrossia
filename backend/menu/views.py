from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import product
from .serializers import productSerializer

@api_view(['POST'])
def addProduct(request):
    serializer = productSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    productData = productSerializer(instance)
    return Response (productData.data)

@api_view(['GET'])
def getAllProducts(request):
    allProducts = product.objects.all()
    serializer = productSerializer(allProducts, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def updateProduct(request, id):
    prod = get_object_or_404(product, pk=id)
    # Permitir actualización parcial de name y/o price
    data = {}
    if 'name' in request.data:
        data['name'] = request.data['name']
    if 'price' in request.data:
        data['price'] = request.data['price']
    serializer = productSerializer(prod, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
