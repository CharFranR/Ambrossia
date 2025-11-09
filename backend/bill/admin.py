from django.contrib import admin
from .models import bill

# Register your models here.

@admin.register(bill)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "createdAt", "closedAt", "amount", "IVA", "discount", "total")
    list_filter = ("status",)
    search_fields = ("id",)