from django.db import models

class product (models.Model):
    name = models.CharField(max_length = 200)
    price =  models.IntegerField()