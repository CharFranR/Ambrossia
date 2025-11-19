from django.contrib import admin
from .models import cashRegister, cashMovement

@admin.register(cashRegister)
class CashRegisterAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "cashierId", "opened_at", "closed_at")
    search_fields = ("id", "cashierId")
    list_filter = ("status", "cashierId")

@admin.register(cashMovement)
class cashMovementAdmin(admin.ModelAdmin):
    list_display = ("cash_inflow", "cash_outflow", "amount", "method", "description",
                    "created_at", "denominations", "cashierId")
    search_fields = ("cashierId", "created_at")
    list_filter = ("amount", "cashierId")