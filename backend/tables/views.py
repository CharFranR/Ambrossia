from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import table, order, orderItem
from .serializers import tableSerializer, orderSerializer, orderItemSerializer, OrderItemLegacySerializer
from .websocketService import tableStateNotification

class TableViewSet(viewsets.ModelViewSet):
    queryset = table.objects.all()
    serializer_class = tableSerializer

    # Sobrescribir create() para replicar addTable
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        # Retornar datos serializados
        return Response(self.get_serializer(instance).data)

    # Acción personalizada para actualizar status (similar a updateStatusPerTable)
    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        table_obj = self.get_object()
        new_status = request.data.get('new_status')
        if new_status:
            table_obj.status = new_status
            table_obj.save()
            # Notificar cambios vía websocket
            try:
                tableStateNotification()
            except Exception:
                pass
        serializer = self.get_serializer(table_obj)
        return Response(serializer.data)

    # Acción personalizada para agregar órdenes a una mesa (similar a addOrder)
    @action(detail=True, methods=['post'])
    def add_order(self, request, pk=None):
        """
        Create order items for a table.
        Expects: [{"product": product_id, "quantity": qty, "note": "optional"}]
        Returns: Legacy format order items with backward compatibility
        """
        table_obj = self.get_object()
        table_obj.status = 'occupied'
        table_obj.save()
        # Notificar cambios
        try:
            tableStateNotification()
        except Exception:
            pass

        # Create a single order for this table (order header)
        order_obj = order.objects.create(
            tableId=table_obj,
            status='notCooking',
            waiterId=request.data.get('waiterId', 1) if isinstance(request.data, dict) else 1
        )

        # Create order items from the request
        order_items = []
        items_data = request.data if isinstance(request.data, list) else [request.data]
        
        for item_data in items_data:
            product_id = item_data.get('product')
            quantity = item_data.get('quantity', 1)
            note = item_data.get('note', '')
            
            if not product_id:
                continue
                
            from menu.models import product
            product_obj = get_object_or_404(product, pk=product_id)
            
            order_item = orderItem.objects.create(
                orderId=order_obj,
                productId=product_obj,
                quantity=quantity,
                note=note
            )
            order_items.append(order_item)

        # Return in legacy format for backward compatibility
        serializer = OrderItemLegacySerializer(order_items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        """Devuelve todas las órdenes de esta mesa"""
        table_obj = self.get_object()
        orders = table_obj.order_set.all() 
        serializer = orderSerializer(orders, many=True)
        return Response(serializer.data)
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = order.objects.all()
    serializer_class = orderSerializer