from django.db import models
from menu.models import product

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
    bill = models.ForeignKey('bill', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    STATUS_CHOICES = [
        ('notcooking','notCooking'),
        ('cooking', 'Cooking'),
        ('ready', 'Ready'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notCooking')
    createdAt = models.DateTimeField(auto_now_add=True)
    closedAt = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)
    

class bill(models.Model):
    STATUS_CHOICES = [
        ('notPayed', 'NotPayed'),
        ('payed', 'Payed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notPayed')
    createdAt = models.DateTimeField(auto_now_add=True)
    closedAt = models.DateTimeField(null=True, blank=True)