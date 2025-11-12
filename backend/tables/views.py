from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import table, order
from .serializers import tableSerializer, orderSerializer
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
        table_obj = self.get_object()
        table_obj.status = 'occupied'
        table_obj.save()
        # Notificar cambios
        try:
            tableStateNotification()
        except Exception:
            pass

        instances = []
        data = request.data.copy()
        for item in data:
            item['table'] = pk
            serializer = orderSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            instances.append(serializer.save())

        return Response(orderSerializer(instances, many=True).data)
    
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