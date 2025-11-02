from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import table, order, bill
from .serializers import tableSerializer, billSerializer, orderSerializer
from .websocketService import tableStateNotification

from channels.consumer import SyncConsumer


def _safe_notify_tables():
    """Best-effort notify over websockets; ignore errors in test/dev."""
    try:
        tableStateNotification()
    except Exception:
        # Notifications are non-critical for API correctness
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
    _safe_notify_tables()
    return Response(serializer.data)

@api_view(['GET'])
def getNotPayedBills (request):
    # mostrar facturaciones abiertas
    notPayedBills = bill.objects.filter(status='notPayed')
    serializer = billSerializer(notPayedBills, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPayedBills (request):
    # mostrar facturaciones cerradas
    payed_bills = bill.objects.filter(status='payed')
    serializer = billSerializer(payed_bills, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addOrder (request, id):
    # cambiamos el estatus de la mesa a ocupado
    table_obj = get_object_or_404(table, pk=id)
    table_obj.status = 'occupied'
    table_obj.save()
    _safe_notify_tables()
    # creamos las ordenes de cada mesa
    data = request.data.copy()
    data['table'] = id
    serializer = orderSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    orderData = orderSerializer(instance).data
    return Response(orderData)


# Endpoint para crear una factura asociada a una mesa
@api_view(['POST'])
def createBill(request, table_id):
    # Obtiene todas las órdenes de la mesa que no tienen bill asociada
    orders = order.objects.filter(table_id=table_id, bill__isnull=True)
    if not orders.exists():
        return Response({'error': 'No hay órdenes para esta mesa'}, status=400)
    # Crea una bill y asocia todas las órdenes a esa factura
    bill_obj = bill.objects.create(status='notPayed')
    for ord in orders:
        ord.bill = bill_obj
        ord.save()
    serializer = billSerializer(bill_obj)
    return Response(serializer.data)

# Endpoint para cambiar el status de la factura
@api_view(['PUT'])
def updateBillStatus(request, bill_id):
    new_status = request.data.get('status')
    if new_status not in ['notPayed', 'payed']:
        return Response({'error': 'Status inválido'}, status=400)
    bill_obj = get_object_or_404(bill, pk=bill_id)
    bill_obj.status = new_status
    bill_obj.save()
    serializer = billSerializer(bill_obj)

    return Response(serializer.data)