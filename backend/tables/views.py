from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import table, order
from bill.models import bill
from .serializers import tableSerializer, orderSerializer
from .websocketService import tableStateNotification
from channels.consumer import SyncConsumer
from .websocketService import ordersNotification
from users.permissions import IsMesero
from rest_framework.decorators import action

class tablesViewSet(viewsets.ViewSet):
    # permission_classes = [IsMesero]
    @action(detail=True, methods=['post'])
    def addTable(request):
        serializer = tableSerializer(data = {})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        productData = tableSerializer(instance).data
        return Response(productData)

    @action(detail=True, methods=['get'])
    def getStatusPerTable(request,id):
        tableObj = get_object_or_404(table, pk=id)
        serializer = tableSerializer (tableObj)
        return Response(serializer.data)

    # @api_view(['Get'])
    # def getAllStatus(resquet):
    #     all_tables = table.objects.all()
    #     serializer = tableSerializer(all_tables, many=True)
    #     return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def updateStatusPerTable(request, id):
        new_status = request.data.get('new_status')
        tableObj = get_object_or_404(table, pk=id)
        tableObj.status = new_status
        tableObj.save()
        serializer = tableSerializer(tableObj)

        # Notificamos a los meseros mediante el websocket
        tableStateNotification()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def addOrder (request, id):
        instance = list ()
        # cambiamos el estatus de la mesa a ocupado
        table_obj = get_object_or_404(table, pk=id)
        table_obj.status = 'occupied'
        table_obj.save()

        # Notificamos a los meseros mediante el websocket

        tableStateNotification()
        # creamos las ordenes de cada mesa
        data = request.data.copy()
        for item in data:
            dataContent = item.copy()
            dataContent['table'] = id
            serializer = orderSerializer(data=dataContent)
            serializer.is_valid(raise_exception=True)
            instance.append(serializer.save())
        orderData = orderSerializer(instance, many=True).data

        # Notificamos a cocina mediante el websocket
        ordersNotification()

        return Response(orderData)