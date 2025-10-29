from django.db import models

class table(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('in_cleaning', 'In Cleaning'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

class bill(models.Model):
    STATUS_CHOICES = [
        ('notPayed', 'NotPayed'),
        ('payed', 'Payed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notPayed')
    createdAt = models.DateTimeField(auto_now_add=True)
    closedAt = models.DateTimeField(null=True, blank=True)
    table = models.ForeignKey(table, on_delete=models.SET_NULL, null=True, blank=True)

class order(models.Model):
    STATUS_CHOICES = [
        ('notcooking','notCooking'),
        ('cooking', 'Cooking'),
        ('ready', 'Ready'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notCooking')
    createdAt = models.DateTimeField(auto_now_add=True)
    closedAt = models.DateTimeField(null=True, blank=True)

class product(models.Model):
    # Luego tendrá su propia app, de manera provicional está aquí
    name = models.CharField(max_length=20)
    price = models.IntegerField()

class orderItem(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    bill = models.ForeignKey('Bill', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')