from rest_framework import serializers
from django.utils import timezone
from .models import cashRegister


class CashRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = cashRegister
        fields = ("id", "createdAt", "closedAt", "status", "cashierId")
        read_only_fields = ("createdAt",)

    def create(self, validated_data):
        return cashRegister.objects.create(**validated_data)
