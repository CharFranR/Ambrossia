from django.db import models

class table(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('in_cleaning', 'In Cleaning'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    tableNumer = models.IntegerField()

class order(models.Model):

    STATUS_CHOICES = [
        ('notCooking','notCooking'),
        ('cooking', 'Cooking'),
        ('ready', 'Ready'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notCooking')
    tableId = models.ForeignKey(table, on_delete= models.CASCADE)
    # Use a lazy string reference to avoid circular import with bill.models
    billId = models.ForeignKey('bill.bill', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(null=True, blank=True)
    waiterId = models.IntegerField()