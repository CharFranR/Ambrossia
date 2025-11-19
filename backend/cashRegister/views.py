from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import cashRegister, cashMovement, billsQuantity
from .serializers import CashRegisterSerializer, cashMovementSerializer, billsQuantitySerilizer
from users.permissions import IsAdmin, IsCaja


class CashRegisterViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar cajas registradoras.
    """
    queryset = cashRegister.objects.all()
    serializer_class = CashRegisterSerializer

    def get_permissions(self):
        if self.action in ['open_register', 'close_register']:
            return [IsCaja()]
        return [IsAdmin()]

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

    def get_permissions(self):
        if self.action == 'create':
            return [IsCaja()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return super().get_permissions()

class BillsQuantityViewSet(viewsets.ModelViewSet):
    queryset = billsQuantity.objects.all()
    serializer_class = billsQuantitySerilizer

    def get_permissions(self):
        if self.action == 'create':
            return [IsCaja()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return super().get_permissions()