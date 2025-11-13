from rest_framework import viewsets
from .models import bill
from tables.models import order, table, orderItem
from rest_framework.response import Response
from .serializers import billSerializer
from rest_framework.decorators import action
from users.permissions import IsCaja
from django.shortcuts import get_object_or_404
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class BillViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsCaja]
    queryset = bill.objects.all()
    serializer_class = billSerializer

    @action(detail=False, methods=['get'])
    def getNotPayedBills (self, request):
        # mostrar facturaciones abiertas
        notPayedBills = bill.objects.filter(status='notPayed')
        serializer = billSerializer(notPayedBills, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def getPayedBills (self, request):
        # mostrar facturaciones cerradas
        payed_bills = bill.objects.filter(status='payed')
        serializer = billSerializer(payed_bills, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='createBill/(?P<table_id>[^/.]+)')
    def createBill(self, request, table_id):
        """
        Create a bill for all unbilled orders from a table.
        Works with the new order/orderItem model structure.
        """
        # Get the table object
        table_obj = get_object_or_404(table, pk=table_id)
        
        # Obtiene todas las órdenes de la mesa que no tienen bill asociada
        orders = order.objects.filter(tableId=table_obj, billId__isnull=True)
        if not orders.exists():
            return Response({'error': 'No hay órdenes para esta mesa'}, status=400)

        # Crea una bill y asocia todas las órdenes a esa factura
        billObj = bill.objects.create(
            status='notPayed',
            tableId=table_obj,
            paidAmount=0,
            paymentMethod='',
            cashier='',
            total=0
        )
        
        orderDetails = []
        total_amount = 0
        
        # Iterate through orders and their items
        for ord in orders:
            # Get all order items for this order
            items = orderItem.objects.filter(orderId=ord)
            
            for item in items:
                amount = item.quantity * item.productId.price
                total_amount += amount
                
                orderDetails.append({
                    'product': item.productId.name,
                    'price': item.productId.price,
                    'quantity': item.quantity,
                    'amount': amount
                })
            
            # Associate order with bill
            ord.billId = billObj
            ord.save()
        
        billObj.paidAmount = total_amount
        
        # calcular IVA
        billObj.IVA = int(0.15 * total_amount)

        # aplicar descuentos (como si dieran)
        discount = request.data.get('discount', 0) # El descuento va en porcentaje
        billObj.discount = total_amount * (int(discount)/100) if discount else 0

        # Calcular precio final a pagar
        billObj.total = round(total_amount + billObj.IVA - billObj.discount, 2)
        billObj.save()

        pdfBuffer = billPDf(orderDetails, billObj.IVA, billObj.discount, billObj.total, table_id)
        pdfPath = f"factura{billObj.id}.pdf"

        with open(pdfPath, "wb") as f:
            f.write(pdfBuffer.getvalue())

        serializer = billSerializer(billObj)
        return Response({
            'bill': serializer.data,
            'orders': orderDetails
        })

    @action(detail=False, methods=['put'], url_path='updateBill/(?P<bill_id>[^/.]+)')
    def updateBill(self, request, bill_id):
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
        
    @action(detail=False, methods=['put'], url_path='updateBillStatus/(?P<bill_id>[^/.]+)')
    def updateBillStatus(self, request, bill_id):
        new_status = request.data.get('status')
        if new_status not in ['notPayed', 'payed']:
            return Response({'error': 'Status inválido'}, status=400)
        billObj = get_object_or_404(bill, pk=bill_id)
        billObj.status = new_status
        billObj.save()
        serializer = billSerializer(billObj)

        return Response(serializer.data)


def billPDf(orderDetails, IVA, discount, total, table_id):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 800, "RESTAURANTE AMBROSSIA")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 780, f"Mesa {table_id}")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 765, "Factura")
    c.line(50, 760, 500, 760)  # Línea debajo de "Factura"

    # Encabezados de la tabla
    y = 740  # Espaciado mayor desde la línea superior
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Producto")
    c.drawString(200, y, "Precio")
    c.drawString(300, y, "Cantidad")
    c.drawString(400, y, "Importe (C$)")
    c.setFont("Helvetica", 12)
    y -= 20
    c.line(50, y + 12, 500, y + 12)  # Línea debajo de encabezados

    # Imprimir cada producto en la factura
    for detalle in orderDetails:
        c.drawString(50, y, f"{detalle['product']}")
        c.drawString(200, y, f"{detalle['price']}")
        c.drawString(300, y, f"{detalle['quantity']}")
        c.drawString(400, y, f"{detalle['amount']:.2f}")
        y -= 20

    # Línea antes de totales
    c.line(50, y+10, 500, y+10)

    # Totales
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(200, y, "Subtotal:")
    c.drawString(300, y, f"{sum(d['amount'] for d in orderDetails):.2f}")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(200, y, "IVA (15%):")
    c.drawString(300, y, f"{IVA:.2f}")
    y -= 20
    c.drawString(200, y, "Descuento:")
    c.drawString(300, y, f"{discount:.2f}")
    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, y, "Total:")
    c.drawString(300, y, f"{total:.2f}")

    c.save()
    buffer.seek(0)
    return buffer