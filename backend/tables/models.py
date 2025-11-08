from django.db import models
from menu.models import product
from bill.models import bill

class table(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('in_cleaning', 'In Cleaning'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

class order(models.Model):
    table = models.ForeignKey(table, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField(default=1) # ok, ahora me obliga a poderles un default, antes no que yo recuerde
    bill = models.ForeignKey(bill, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    STATUS_CHOICES = [
        ('notCooking','notCooking'),
        ('cooking', 'Cooking'),
        ('ready', 'Ready'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notCooking')
    createdAt = models.DateTimeField(auto_now_add=True)
    closedAt = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)