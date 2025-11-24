from rest_framework import serializers
from .models import CashRegister, CashMovement, BillsQuantity

class CashRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRegister
        fields = ("id", "opened_at", "closed_at", "status", "cashierId")
        read_only_fields = ("opened_at", "closed_at")

class CashMovementSerializer(serializers.ModelSerializer):
    cashRegisterNumber = serializers.PrimaryKeyRelatedField(queryset = CashRegister.objects.all())
    class Meta:
        model = CashMovement
        fields = ("id", "cash_inflow", "cash_outflow", "amount", "method", "description", 
                  "created_at", "denominations", "cashierId", "cashRegisterNumber")

class BillsQuantitySerializer(serializers.ModelSerializer):
    cash_register = serializers.PrimaryKeyRelatedField(queryset=CashRegister.objects.all())
    class Meta:
        model = BillsQuantity
        fields = ("id", "denomination", "quantity", "cash_register")

class ChangeOutputSerializer(serializers.Serializer):
    denomination = serializers.IntegerField()
    quantity = serializers.IntegerField()