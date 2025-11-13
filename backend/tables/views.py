from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import table, order, orderItem
from .serializers import tableSerializer, orderSerializer, orderItemSerializer
from .websocketService import tableStateNotification


class TableViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar mesas del restaurante.
    """
    queryset = table.objects.all()
    serializer_class = tableSerializer

    def create(self, request, *args, **kwargs):
        """
        Crear una nueva mesa.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            self.get_serializer(instance).data, 
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        """
        Actualizar el estado de una mesa.
        Estados posibles: 'available', 'occupied', 'reserved', 'in_cleaning'
        """
        table_obj = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'status es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_status not in ['available', 'occupied', 'reserved', 'in_cleaning']:
            return Response(
                {'error': 'status inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        table_obj.status = new_status
        table_obj.save()
        
        # Notificar cambios vía websocket
        try:
            tableStateNotification()
        except Exception:
            pass
        
        serializer = self.get_serializer(table_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_order(self, request, pk=None):
        """
        Agregar una orden a una mesa.
        La orden incluye el waiterId que referencia al sistema de permisos.
        """
        table_obj = self.get_object()
        
        # waiterId es IntegerField - referencia al sistema de permisos de users app
        # Para obtener el usuario actual autenticado, usar: request.user.id
        # y validar que tiene permiso 'mesero_access' mediante users.permissions.IsMesero
        
        table_obj.status = 'occupied'
        table_obj.save()
        
        # Notificar cambios
        try:
            tableStateNotification()
        except Exception:
            pass

        # Crear la orden
        order_data = request.data.copy()
        order_data['tableId'] = pk
        
        serializer = orderSerializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        order_instance = serializer.save()

        return Response(
            orderSerializer(order_instance).data, 
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def get_orders(self, request, pk=None):
        """
        Obtener todas las órdenes de una mesa específica.
        """
        table_obj = self.get_object()
        orders = order.objects.filter(tableId=table_obj)
        serializer = orderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar órdenes.
    """
    queryset = order.objects.all()
    serializer_class = orderSerializer

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        """
        Actualizar el estado de una orden.
        Estados posibles: 'notCooking', 'cooking', 'ready'
        """
        order_obj = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'status es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_status not in ['notCooking', 'cooking', 'ready']:
            return Response(
                {'error': 'status inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order_obj.status = new_status
        order_obj.updatedAt = timezone.now()
        order_obj.save()
        
        serializer = orderSerializer(order_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_items(self, request, pk=None):
        """
        Obtener todos los items de una orden específica.
        """
        order_obj = self.get_object()
        items = orderItem.objects.filter(orderId=order_obj)
        serializer = orderItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """
        Agregar un item a una orden existente.
        """
        order_obj = self.get_object()
        
        item_data = request.data.copy()
        item_data['orderId'] = pk
        
        serializer = orderItemSerializer(data=item_data)
        serializer.is_valid(raise_exception=True)
        item_instance = serializer.save()
        
        return Response(
            orderItemSerializer(item_instance).data, 
            status=status.HTTP_201_CREATED
        )


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar items de órdenes.
    """
    queryset = orderItem.objects.all()
    serializer_class = orderItemSerializer