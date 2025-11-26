from django.db import models
from menu.models import Product

class table(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('in_cleaning', 'In Cleaning'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    tableNumber = models.IntegerField()

class order(models.Model):

    STATUS_CHOICES = [
        ('notCooking','notCooking'),
        ('cooking', 'Cooking'),
        ('ready', 'Ready'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notCooking')
    tableId = models.ForeignKey(table, on_delete= models.CASCADE, null=True, blank=True)
    billId = models.ForeignKey('bill.bill', on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(null=True, blank=True)
    waiterId = models.IntegerField(null=True, blank=True)

class orderItem(models.Model):
    orderId = models.ForeignKey(order, on_delete=models.CASCADE)
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    note = models.TextField(null=True, blank=True)