from django.db import models
from django.utils import timezone
from products.models import Product

class Debtor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    # This calculates the remaining balance automatically
    @property
    def balance(self):
        return self.total_amount - self.amount_paid

    def __str__(self):
        return f"{self.name} - {self.product.name}"

class PartialPayment(models.Model):
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.debtor.name} paid {self.amount_paid}"