from django.db import models

# Tipos
class inventoryProductType(models.Model):
    name = models.CharField(max_length=200)

class inventoryMovementType(models.Model):
    name = models.CharField(max_length=200)

# Tablas
class inventoryProduct(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    type = models.ForeignKey(inventoryProductType, on_delete=models.CASCADE)
    lastUpdated = models.DateTimeField(auto_now_add=True)

class inventoryMovement(models.Model):
    itemId = models.ForeignKey(inventoryProduct, on_delete=models.CASCADE, null=True, blank=True)
    movementType = models.ForeignKey(inventoryMovementType, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    userId = models.IntegerField()