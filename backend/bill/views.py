from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import bill
from .serializers import billSerializer
from tables.models import order

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

# Endpoint para crear una factura asociada a una mesa
@api_view(['POST'])
def createBill(request, table_id):
    # Obtiene todas las órdenes de la mesa que no tienen bill asociada
    orders = order.objects.filter(table_id=table_id, bill__isnull=True)
    if not orders.exists():
        return Response({'error': 'No hay órdenes para esta mesa'}, status=400)

    # Crea una bill y asocia todas las órdenes a esa factura
    billObj = bill.objects.create(status='notPayed')
    for ord in orders:
        bill_obj.amount += (ord.quantity * ord.product.price)
        ord.bill = bill_obj
        ord.save()
    
    # calcular IVA
    billObj.IVA = 0.15 * bill_obj.amount

    # aplicar descuentos (como si dieran)
    discount = request.data.get('discount', 0) # El descuento va en porcentaje, ojo ahi
    billObj.discount = bill_obj.amount * (int(discount)/100)

    # Calcular precio final a pagar

    billObj.total = round (bill_obj.amount + bill_obj.IVA - bill_obj.discount, 2)
    billObj.save()

    serializer = billSerializer(bill_obj)
    return Response(serializer.data)


@api_view(['PUT'])
def updateBill(request, bill_id):
    billObj = get_object_or_404(bill, pk=bill_id)

    if bill.status == 'payed':
        return Response('No es posible moficiar una factura ya pagada')

    IVA = billObj.amount * (int (request.data.get('IVA', billObj.IVA))/100)
    discount = float (request.data.get('discount', billObj.discount))

    total = round (billObj.amount + IVA - discount, 2) # Abria que reutilizar codigo, pero para despues

    billObj.IVA = IVA
    billObj.discount = discount
    billObj.total = total

    billObj.save()

    serializer = billSerializer(billObj)

    return Response(serializer.data)

# Endpoint para cambiar el status de la factura
@api_view(['PUT'])
def updateBillStatus(request, bill_id):
    new_status = request.data.get('status')
    if new_status not in ['notPayed', 'payed']:
        return Response({'error': 'Status inválido'}, status=400)
    billObj = get_object_or_404(bill, pk=bill_id)
    billObj.status = new_status
    billObj.save()
    serializer = billSerializer(billObj)

    return Response(serializer.data)
