from django.db import models

class cashRegister (models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    closedAt = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=200)
    # cashierId
