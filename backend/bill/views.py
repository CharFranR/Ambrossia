from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os, tempfile

from .models import bill
from .serializers import billSerializer
from tables.models import order, orderItem


class BillViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar facturas.
    Solo accesible por usuarios con permisos de caja.
    """
    # permission_classes = [IsCaja]
    queryset = bill.objects.all()
    serializer_class = billSerializer

    @action(detail=False, methods=['get'])
    def get_not_payed_bills(self, request):
        """
        Obtener todas las facturas pendientes de pago.
        """
        not_payed_bills = bill.objects.filter(status='notPayed')
        serializer = billSerializer(not_payed_bills, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_payed_bills(self, request):
        """
        Obtener todas las facturas pagadas.
        """
        payed_bills = bill.objects.filter(status='payed')
        serializer = billSerializer(payed_bills, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create_bill/(?P<table_id>[^/.]+)')
    def create_bill(self, request, table_id=None):
        """
        Crear una factura para una mesa específica.
        Incluye cálculo de IVA, descuentos y generación de PDF.
        
        El campo cashier es CharField - referencia al sistema de permisos de users app.
        Para obtener el usuario actual autenticado, usar: request.user.id
        y validar que tiene permiso 'caja_access' mediante users.permissions.IsCaja
        """
        # Obtener el cashier del request
        cashier = request.data.get('cashier', '')
        payment_method = request.data.get('paymentMethod', 'cash')
        
        # Obtener todas las órdenes de la mesa que no tienen bill asociada
        orders = order.objects.filter(tableId=table_id, billId__isnull=True)
        
        if not orders.exists():
            return Response(
                {'error': 'No hay órdenes para esta mesa'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear la factura
        bill_obj = bill.objects.create(
            tableId_id=table_id,
            status='notPayed',
            paymentMethod=payment_method,
            cashier=cashier,
            paidAmount=0,
            IVA = 0,
            discount = 0,
            total=0
        )

        # Calcular el monto total basado en los items de las órdenes
        order_details = []
        subtotal = 0
        
        for ord in orders:
            # Obtener items de esta orden
            items = orderItem.objects.filter(orderId=ord)
            for item in items:
                amount = item.quantity * item.productId.price
                bill_obj.paidAmount += amount
                
                order_details.append({
                    'product': item.productId.name,
                    'price': item.productId.price,
                    'quantity': item.quantity,
                    'amount': amount
                })
            
            # Asociar orden a la factura
            ord.billId = bill_obj
            ord.save()
        
        # Calcular IVA (15%)
        bill_obj.IVA = round(0.15 * bill_obj.paidAmount, 2)

        # Aplicar descuentos
        discount_percent = float(request.data.get('discount', 0))
        bill_obj.discount = round(bill_obj.paidAmount * (discount_percent / 100), 2)

        # Calcular precio final a pagar
        bill_obj.total = round(bill_obj.paidAmount + bill_obj.IVA - bill_obj.discount, 2)
        bill_obj.save()

        # Generar PDF
        try:
            pdf_buffer = generate_bill_pdf(
                order_details, 
                bill_obj.IVA, 
                bill_obj.discount, 
                bill_obj.total, 
                table_id
            )
            
            pdf_path = f"/factura_{getattr(bill_obj, 'pk')}.pdf"
            
            with open(pdf_path, "wb") as f:
                f.write(pdf_buffer.getvalue())
        except Exception as e:
            # Si falla la generación del PDF, continuar sin él
            pass

        serializer = billSerializer(bill_obj)
        return Response({
            'bill': serializer.data,
            'orders': order_details
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update_bill(self, request, pk=None):
        """
        Actualizar una factura existente (IVA, descuento, etc).
        No se puede modificar una factura ya pagada.
        """
        bill_obj = self.get_object()

        if bill_obj.status == 'payed':
            return Response(
                {'error': 'No es posible modificar una factura ya pagada'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Recalcular con los nuevos valores
        subtotal = bill_obj.paidAmount
        
        # IVA
        iva_percent = float(request.data.get('IVA', 15))
        bill_obj.IVA = round(subtotal * (iva_percent / 100), 2)
        
        # Descuento
        discount = float(request.data.get('discount', bill_obj.discount or 0))
        bill_obj.discount = discount

        # Total
        bill_obj.total = round(subtotal + bill_obj.IVA - bill_obj.discount, 2)
        bill_obj.save()

        serializer = billSerializer(bill_obj)
        return Response(serializer.data)
        
    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        """
        Actualizar el estado de pago de una factura.
        Cuando se marca como 'payed', se registra la fecha de cierre.
        """
        bill_obj = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in ['notPayed', 'payed']:
            return Response(
                {'error': 'Status inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        bill_obj.status = new_status
        
        if new_status == 'payed':
            bill_obj.closedAt = timezone.now()
            # Actualizar el monto pagado si se proporciona
            paid_amount = request.data.get('paidAmount')
            if paid_amount:
                bill_obj.paidAmount = float(paid_amount)
        
        bill_obj.save()
        serializer = billSerializer(bill_obj)
        return Response(serializer.data)


def generate_bill_pdf(order_details, iva, discount, total, table_id):
    """
    Generar un PDF de la factura.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Encabezado
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 800, "RESTAURANTE AMBROSSIA")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 780, f"Mesa {table_id}")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 765, "Factura")
    c.line(50, 760, 500, 760)

    # Encabezados de la tabla
    y = 740
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Producto")
    c.drawString(200, y, "Precio")
    c.drawString(300, y, "Cantidad")
    c.drawString(400, y, "Importe (C$)")
    c.setFont("Helvetica", 12)
    y -= 20
    c.line(50, y + 12, 500, y + 12)

    # Detalles de productos
    for detalle in order_details:
        c.drawString(50, y, f"{detalle['product']}")
        c.drawString(200, y, f"{detalle['price']}")
        c.drawString(300, y, f"{detalle['quantity']}")
        c.drawString(400, y, f"{detalle['amount']:.2f}")
        y -= 20

    # Línea antes de totales
    c.line(50, y + 10, 500, y + 10)

    # Totales
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(200, y, "Subtotal:")
    c.drawString(300, y, f"{sum(d['amount'] for d in order_details):.2f}")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(200, y, "IVA (15%):")
    c.drawString(300, y, f"{iva:.2f}")
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