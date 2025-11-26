from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import (
    inventorySupply,
    inventorySupplyType,
    inventoryMovementType,
    inventoryMovement,
)
from .serializers import (
    inventorySupplySerializer,
    InventorySupplyTypeSerializer,
    InventoryMovementTypeSerializer,
    InventoryMovementSerializer,
)

class inventorySupplyViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar productos en inventario.
    """
    queryset = inventorySupply.objects.all()
    serializer_class = inventorySupplySerializer

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        """
        Agregar un nuevo producto al inventario.
        """
        serializer = inventorySupplySerializer(data=request.data, context = {'userId'})
        serializer.is_valid(raise_exception=True)
        serializer.save(lastUpdated=timezone.now())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update_quantity(self, request, pk=None):
        """
        Actualizar la cantidad de un producto en inventario.
        """
        product = self.get_object()
        quantity = request.data.get('quantity')
        
        if quantity is None:
            return Response(
                {'error': 'quantity es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.quantity = quantity
        product.lastUpdated = timezone.now()
        product.save()
        
        serializer = InventoryProductSerializer(product)
        return Response(serializer.data)


class InventorySupplyTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar tipos de items en inventario.
    """
    queryset = inventorySupplyType.objects.all()
    serializer_class = InventorySupplyTypeSerializer


class InventoryMovementTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar tipos de movimientos en inventario.
    """
    queryset = inventoryMovementType.objects.all()
    serializer_class = InventoryMovementTypeSerializer

class InventoryMovementViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar movimientos de inventario.
    """
    queryset = inventoryMovement.objects.all()
    serializer_class = InventoryMovementSerializer

    @action(detail=False, methods=['post'])
    def create_movement(self, request):
        """
        Crear un nuevo movimiento de inventario.
        """
        serializer = InventoryMovementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdAt=timezone.now())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def get_movements_by_item(self, request):
        """
        Obtener todos los movimientos para un item específico.
        """
        item_id = request.query_params.get('itemId')
        
        if not item_id:
            return Response(
                {'error': 'itemId es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        movements = inventoryMovement.objects.filter(itemId=item_id)
        serializer = InventoryMovementSerializer(movements, many=True)
        return Response(serializer.data)