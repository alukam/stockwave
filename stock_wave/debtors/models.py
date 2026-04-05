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
    due_date = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def balance(self):
        return self.total_amount - self.amount_paid

    def save(self, *args, **kwargs):
        if self.balance <= 0:
            self.is_paid = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.balance} UGX"

class PartialPayment(models.Model):
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # When a payment is saved, update the Debtor's total amount_paid
        self.debtor.amount_paid += self.amount_paid
        self.debtor.save() # This also triggers the Debtor's is_paid check
        super().save(*args, **kwargs)