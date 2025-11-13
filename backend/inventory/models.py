from django.db import models

class inventoryProduct(models.Model):
    productId = models.IntegerField()
    quantity = models.IntegerField()
    lastUpdated = models.DateTimeField()

class inventoryIngredient(models.Model):
    ingredientId = models.IntegerField()
    quantity = models.IntegerField()
    lastUpdated = models.DateTimeField()

class inventoryItemType(models.Model):
    name = models.CharField(max_length=200)

class inventoryMovementType(models.Model):
    name = models.CharField(max_length=200)

class inventoryMovement(models.Model):
    itemType = models.ForeignKey(inventoryItemType, on_delete=models.CASCADE)
    itemId = models.ForeignKey(inventoryProduct, on_delete=models.CASCADE)
    movementType = models.ForeignKey(inventoryMovementType, on_delete=models.CASCADE)
    createdAt = models.DateTimeField()
    # userId = models.ForeignKey(user, on_delete=models.CASCADE)