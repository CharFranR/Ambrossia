from rest_framework import serializers
from .models import table, order, orderItem
from menu.models import product

class tableSerializer(serializers.ModelSerializer):
    class Meta:
        model = table
        fields = ['id', 'status', 'tableNumber']

    def create(self, validated_data):
        # Auto-generate tableNumber if not provided
        if 'tableNumber' not in validated_data:
            last_table = table.objects.order_by('tableNumber').last()
            validated_data['tableNumber'] = (last_table.tableNumber + 1) if last_table else 1
        return table.objects.create(**validated_data)

class orderSerializer(serializers.ModelSerializer):
    tableId = serializers.PrimaryKeyRelatedField(queryset=table.objects.all())
    
    class Meta:
        model = order
        fields = ['id', 'tableId', 'billId', 'status', 'createdAt', 'updatedAt', 'waiterId']

    def create(self, validated_data):
        # Set default waiterId if not provided
        if 'waiterId' not in validated_data:
            validated_data['waiterId'] = 1  # Default waiter
        return order.objects.create(**validated_data)
    
class orderItemSerializer(serializers.ModelSerializer):
    productId = serializers.PrimaryKeyRelatedField(queryset=product.objects.all(), source='productId')
    orderId = serializers.PrimaryKeyRelatedField(queryset=order.objects.all(), required=False, source='orderId')

    class Meta:
        model = orderItem
        fields = ('id', 'orderId', 'productId', 'quantity', 'note')

    def create(self, validated_data):
        # Set default note if not provided
        if 'note' not in validated_data:
            validated_data['note'] = ''
        return orderItem.objects.create(**validated_data)

# Legacy serializer for backward compatibility with old API format
class OrderItemLegacySerializer(serializers.Serializer):
    """
    Serializer for the legacy order format where order items were represented
    as a flat structure with table, product, quantity, etc.
    This maintains backward compatibility while working with the new order/orderItem model.
    """
    id = serializers.IntegerField(read_only=True)
    table = serializers.IntegerField(source='orderId.tableId.id', read_only=True)
    product = serializers.IntegerField(source='productId.id')
    quantity = serializers.IntegerField(default=1)
    status = serializers.CharField(source='orderId.status', read_only=True)
    createdAt = serializers.DateTimeField(source='orderId.createdAt', read_only=True)
    closedAt = serializers.DateTimeField(read_only=True, allow_null=True, required=False)
    note = serializers.CharField(default='', allow_blank=True)
    
    def to_representation(self, instance):
        """Convert orderItem instance to legacy format"""
        return {
            'id': instance.id,
            'table': instance.orderId.tableId.id,
            'product': instance.productId.id,
            'quantity': instance.quantity,
            'status': instance.orderId.status,
            'createdAt': instance.orderId.createdAt,
            'closedAt': None,  # order model doesn't have closedAt
            'note': instance.note
        }