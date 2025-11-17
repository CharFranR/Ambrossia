from django.contrib import admin
from .models import table, order

# Register your models here.

@admin.register(table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("id", "status")
    list_filter = ("status",)
    search_fields = ("id",)

@admin.register(order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "tableId", "billId", "status", "createdAt", "updatedAt", "waiterId")
    list_filter = ("status",)
    search_fields = ("tableId__id", "waiterId")