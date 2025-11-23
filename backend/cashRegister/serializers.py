from rest_framework import serializers
from .models import cashRegister, cashMovement, billsQuantity

class CashRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = cashRegister
        fields = ("id", "opened_at", "closed_at", "status", "cashierId")
        read_only_fields = ("opened_at", "closed_at")

class cashMovementSerializer(serializers.ModelSerializer):
    cashRegisterNumber = serializers.PrimaryKeyRelatedField(queryset = cashRegister.objects.all())
    class Meta:
        model = cashMovement
        fields = ("id", "cash_inflow", "cash_outflow", "amount", "method", "description", 
                  "created_at", "denominations", "cashierId", "cashRegisterNumber")

class billsQuantitySerilizer(serializers.ModelSerializer):
    class Meta:
        model = billsQuantity
        fields = ("id", "denomination", "quantity")