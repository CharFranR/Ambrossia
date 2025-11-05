from rest_framework import serializers
from .models import bill
from tables.models import order

class billSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = bill
        fields = ['id', 'status','createdAt', 'closedAt', 'orders', 'amount', 'IVA', 'discount', 'total']
        