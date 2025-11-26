from django.db import models

# Tipos
class inventorySupplyType(models.Model):
    name = models.CharField(max_length=200)

class inventoryMovementType(models.Model):
    name = models.CharField(max_length=200)

# Tablas
class inventorySupply(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    type = models.ForeignKey(inventorySupplyType, on_delete=models.CASCADE)
    lastUpdated = models.DateTimeField(auto_now_add=True)

class inventoryMovement(models.Model):
    itemId = models.ForeignKey(inventorySupply, on_delete=models.CASCADE, null=True, blank=True)
    movementType = models.ForeignKey(inventoryMovementType, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    userId = models.IntegerField()