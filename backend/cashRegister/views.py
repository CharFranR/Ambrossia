from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import cashRegister, cashMovement, billsQuantity
from .serializers import CashRegisterSerializer, cashMovementSerializer, billsQuantitySerilizer
from users.permissions import IsAdmin, IsCaja

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

class CashRegisterViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar cajas registradoras.
    """
    queryset = cashRegister.objects.all()
    serializer_class = CashRegisterSerializer

    # def get_permissions(self):
    #     if self.action in ['open_register', 'close_register']:
    #         return [IsCaja()]
    #     return [IsAdmin()]

    @action(detail=False, methods=['post'])
    def open_register(self, request):
        """
        Abrir una nueva caja registradora.
        El cashierId debe ser pasado en el request.
        """
        cashier_id = request.data.get('cashierId')
        
        if not cashier_id:
            return Response(
                {'error': 'cashierId es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar que no haya una caja abierta para este cajero
        open_registers = cashRegister.objects.filter(
            cashierId=cashier_id, 
            status='open'
        )

        if open_registers.exists():
            return Response(
                {'error': 'Ya existe una caja abierta para este cajero'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        register = get_object_or_404(cashRegister, cashier_id = cashier_id) 

        register.status = 'open'
        register.opened_at = timezone.now()
        
        serializer = CashRegisterSerializer(register)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def close_register(self, request, pk=None):
        """
        Cerrar una caja registradora existente.
        """
        register = self.get_object()
        
        if register.status == 'closed':
            return Response(
                {'error': 'La caja ya está cerrada'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        register.status = 'closed'
        register.closedAt = timezone.now()
        register.save()

        generate_daily_report(date = register.closedAt, register_id = register.id)

        try:

            pdf_buffer =  generate_daily_report(date = register.closedAt, register_id= register.pk)
            pdf_path = f"cashMovements/movements_{register.date}.pdf"

            with open(pdf_path, "wb") as f:
                f.write(pdf_buffer.getvalue())
        
        except Exception as e:
            return Response (e)
        
        serializer = CashRegisterSerializer(register)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_open_registers(self, request):
        """
        Obtener todas las cajas registradoras abiertas.
        """
        open_registers = cashRegister.objects.filter(status='open')
        serializer = CashRegisterSerializer(open_registers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_closed_registers(self, request):
        """
        Obtener todas las cajas registradoras cerradas.
        """
        closed_registers = cashRegister.objects.filter(status='closed')
        serializer = CashRegisterSerializer(closed_registers, many=True)
        return Response(serializer.data)     
    
class CashMovementViewSet(viewsets.ModelViewSet):
    queryset = cashMovement.objects.all()
    serializer_class = cashMovementSerializer

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [IsCaja()]
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         return [IsAdmin()]
    #     return super().get_permissions()

class BillsQuantityViewSet(viewsets.ModelViewSet):
    queryset = billsQuantity.objects.all()
    serializer_class = billsQuantitySerilizer

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [IsCaja()]
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         return [IsAdmin()]
    #     return super().get_permissions()
    
def generate_daily_report(date, register_id):

    movements = cashMovement.objects.filter(created_at = date, cashRegisterNumber = register_id)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, f"Reporte Diario Caja {register_id} - {date.date()}")

    # Encabezados
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 80, "ID")
    p.drawString(120, height - 80, "Metodo")
    p.drawString(220, height - 80, "Monto")
    p.drawString(320, height - 80, "Fecha")

    # Listar movimientos
    y = height - 100
    p.setFont("Helvetica", 10)
    for m in movements:
        p.drawString(50, y, str(m.pk))
        p.drawString(120, y, str(m.method))
        p.drawString(220, y, f"${m.amount:.2f}")
        p.drawString(320, y, m.created_at.strftime("%Y-%m-%d %H:%M"))
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50
    
    p.save()