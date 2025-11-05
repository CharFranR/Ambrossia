from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import table, order
from bill.models import bill
from .serializers import tableSerializer, orderSerializer
from .websocketService import tableStateNotification
from channels.consumer import SyncConsumer


def notifyTables():
    try:
        tableStateNotification()
    except Exception:
        pass

@api_view(['POST'])
def addTable(request):
    serializer = tableSerializer(data = {})
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    productData = tableSerializer(instance).data
    return Response(productData)

@api_view(['GET'])
def getStatusPerTable(request,id):
    tableObj = get_object_or_404(table, pk=id)
    serializer = tableSerializer (tableObj)
    return Response(serializer.data)

# @api_view(['Get'])
# def getAllStatus(resquet):
#     all_tables = table.objects.all()
#     serializer = tableSerializer(all_tables, many=True)
#     return Response(serializer.data)

@api_view(['PUT'])
def updateStatusPerTable(request, id):
    new_status = request.data.get('new_status')
    tableObj = get_object_or_404(table, pk=id)
    tableObj.status = new_status
    tableObj.save()
    serializer = tableSerializer(tableObj)
    notifyTables()
    return Response(serializer.data)

@api_view(['POST'])
def addOrder (request, id):
    instance = list ()
    # cambiamos el estatus de la mesa a ocupado
    table_obj = get_object_or_404(table, pk=id)
    table_obj.status = 'occupied'
    table_obj.save()
    notifyTables()
    # creamos las ordenes de cada mesa
    data = request.data.copy()
    for item in data:
        dataContent = item.copy()
        dataContent['table'] = id
        serializer = orderSerializer(data=dataContent)
        serializer.is_valid(raise_exception=True)
        instance.append(serializer.save())
    orderData = orderSerializer(instance, many=True).data
    return Response(orderData)