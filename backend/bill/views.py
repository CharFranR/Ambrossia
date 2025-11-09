from rest_framework import viewsets
from .models import bill
from .serializers import billSerializer
from rest_framework.decorators import action
from users.permissions import IsCaja

class BillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCaja]
    queryset = bill.objects.all()
    serializer_class = billSerializer

    @action(detail=False, methods=['get'])
    def getNotPayedBills (request):
        # mostrar facturaciones abiertas
        notPayedBills = bill.objects.filter(status='notPayed')
        serializer = billSerializer(notPayedBills, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def getPayedBills (request):
        # mostrar facturaciones cerradas
        payed_bills = bill.objects.filter(status='payed')
        serializer = billSerializer(payed_bills, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def createBill(request, table_id):
        # Obtiene todas las órdenes de la mesa que no tienen bill asociada
        orders = order.objects.filter(table_id=table_id, bill__isnull=True)
        if not orders.exists():
            return Response({'error': 'No hay órdenes para esta mesa'}, status=400)

    @action(detail=False, methods=['update'])
    def updateBill(request, bill_id):
        billObj = get_object_or_404(bill, pk=bill_id)
        
    @action(detail=False, methods=['update'])
    def updateBillStatus(request, bill_id):
        new_status = request.data.get('status')
        if new_status not in ['notPayed', 'payed']:
            return Response({'error': 'Status inválido'}, status=400)
        billObj = get_object_or_404(bill, pk=bill_id)
        billObj.status = new_status
        billObj.save()
        serializer = billSerializer(billObj)
