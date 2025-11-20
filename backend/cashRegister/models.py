from django.db import models
from bill.models import bill

class cashRegister (models.Model):
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=200, default="close")
    cashierId = models.CharField(max_length=200)

class cashMovement(models.Model):
    cash_inflow = models.FloatField(null=True)
    cash_outflow = models.FloatField(null=True)
    amount = models.FloatField()
    method = models.CharField()
    description = models.TextField(default="bill payment")
    created_at = models.DateField()
    denominations = models.JSONField(default=dict)
    cashierId = models.CharField(max_length=200)
    cashRegisterNumber = models.ForeignKey(cashRegister, on_delete= models.CASCADE)
     
class billsQuantity (models.Model):
    bill_5_cordobas = models.IntegerField(default=0)
    bill_10_cordobas = models.IntegerField(default=0)
    bill_20_cordobas = models.IntegerField(default=0)
    bill_50_cordobas = models.IntegerField(default=0)
    bill_100_cordobas = models.IntegerField(default=0)
    bill_200_cordobas = models.IntegerField(default=0)
    bill_500_cordobas = models.IntegerField(default=0)
    bill_1000_cordobas = models.IntegerField(default=0)