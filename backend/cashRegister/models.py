from django.db import models

class CashRegister (models.Model):
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=200, default="close")
    cashierId = models.CharField(max_length=200)

class CashMovement(models.Model):
    cash_inflow = models.FloatField(null=True)
    cash_outflow = models.FloatField(null=True)
    amount = models.FloatField()
    method = models.CharField(max_length=200)
    description = models.TextField(default="bill payment")
    created_at = models.DateTimeField(auto_now_add=True)
    denominations = models.JSONField(default=dict)
    cashierId = models.CharField(max_length=200)
    cashRegisterNumber = models.ForeignKey(CashRegister, on_delete= models.CASCADE)
     
class BillsQuantity (models.Model):
    denomination = models.FloatField(null=True)
    quantity = models.IntegerField(null=True)
    cash_register = models.ForeignKey(CashRegister, on_delete= models.CASCADE, related_name="cash_register")