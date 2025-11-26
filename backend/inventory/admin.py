from django.contrib import admin

from .models import (
    inventorySupply,
    inventorySupplyType,
    inventoryMovementType,
    inventoryMovement,
)

@admin.register(inventorySupply)
class InventorySupplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'type', 'lastUpdated')
    search_fields = ('name',)
    list_filter = ('type',)

@admin.register(inventorySupplyType)
class InventorySupplyTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(inventoryMovementType)
class InventoryMovementTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(inventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ('id', 'itemId', 'movementType', 'createdAt', 'userId')
    list_filter = ('movementType',)
    search_fields = ('itemId__name',)