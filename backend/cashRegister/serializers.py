from rest_framework import serializers
from django.utils import timezone
from .models import cashRegister, cashMovement, billsQuantity


class CashRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = cashRegister
        fields = ("id", "opened_at", "closedAt", "status", "cashierId")
        read_only_fields = ("createdAt")

class cashMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = cashMovement
        fields = ("id", "cash_inflow", "cash_outflow", "amount", "method", "description", 
                  "created_at", "denominations", "cashierId")
        read_only_fields = ("createdAt")

class billsQuantitySerilizer(serializers.ModelSerializer):
    class Meta:
        model = billsQuantity
        fields = ("bill_5_cordobas", "bill_10_cordobas", "bill_20_cordobas", "bill_50_cordobas",
                  "bill_100_cordobas", "bill_200_cordobas", "bill_500_cordobas", "bill_1000_cordobas")
        