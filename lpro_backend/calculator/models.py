from django.db import models
from django.conf import settings


class Operation(models.Model):
    type = models.CharField("Operation type", max_length=100)
    cost = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return self.type


class Record(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name="records")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="records")
    amount = models.DecimalField(max_digits=7, decimal_places=3)
    user_balance = models.DecimalField(max_digits=7, decimal_places=3)
    operation_response = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
