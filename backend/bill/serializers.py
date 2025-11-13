from rest_framework import serializers
from .models import bill
from tables.models import order

class billSerializer(serializers.ModelSerializer):
    # Use order_set as the reverse relationship name from order to bill
    orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='order_set')
    
    class Meta:
        model = bill
        fields = ['id', 'tableId', 'status', 'createdAt', 'closedAt', 'paidAmount', 'paymentMethod', 'cashier', 'IVA', 'discount', 'total', 'orders']
        read_only_fields = ['createdAt']
        