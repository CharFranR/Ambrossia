from django.db import models

class bill(models.Model):
    STATUS_CHOICES = [
        ('notPayed', 'NotPayed'),
        ('payed', 'Payed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notPayed')
    createdAt = models.DateTimeField(auto_now_add=True)
    closedAt = models.DateTimeField(null=True, blank=True) 
    amount = models.FloatField(default=0) 
    IVA = models.FloatField(null=True, blank=True) 
    discount = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True) 