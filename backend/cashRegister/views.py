from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import cashRegister
from .serializers import CashRegisterSerializer


class CashRegisterViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar cajas registradoras.
    """
    queryset = cashRegister.objects.all()
    serializer_class = CashRegisterSerializer

    @action(detail=False, methods=['post'])
    def open_register(self, request):
        """
        Abrir una nueva caja registradora.
        El cashierId debe ser pasado en el request.
        """
        cashier_id = request.data.get('cashierId')
        # cashierId es CharField - referencia al sistema de permisos de users app
        # Para obtener el usuario actual autenticado, usar: request.user.id
        # y validar que tiene permiso 'caja_access' mediante users.permissions.IsCaja
        
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

        register = cashRegister.objects.create(
            cashierId=cashier_id,
            status='open'
        )
        
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
