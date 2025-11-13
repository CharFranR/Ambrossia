from django.contrib import admin
from .models import bill

# Register your models here.

@admin.register(bill)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "tableId", "createdAt", "closedAt", "paidAmount", "paymentMethod")
    list_filter = ("status",)
    search_fields = ("id", "tableId__id")