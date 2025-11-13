from django.db import models

class bill(models.Model):
    STATUS_CHOICES = [
        ('notPayed', 'NotPayed'),
        ('payed', 'Payed'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notPayed')
    tableId = models.ForeignKey('tables.table', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    closedAt = models.DateTimeField(null=True, blank=True)
    paidAmount = models.FloatField(default=0) 
    paymentMethod = models.CharField(max_length=20, blank=True, default='')
    cashier = models.CharField(max_length=200, blank=True, default='')

    # Los siguientes campos no habian sido considerados, mal ahi por el mae qeu hizo los diagramas

    IVA = models.IntegerField(null=True, blank=True, default=0)
    discount = models.FloatField(null=True, blank=True, default=0)
    total = models.FloatField(default=0)