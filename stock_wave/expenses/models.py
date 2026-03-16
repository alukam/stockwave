from django.db import models
from django.conf import settings

class Expense(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    amount = models.BigIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} - {self.amount} UGX"
    