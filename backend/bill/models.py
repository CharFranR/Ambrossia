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
    paymentMethod = models.CharField(max_length=20)
    # cashier = models.ForeignKey(cashier, on_delete= models.CASCADE)
