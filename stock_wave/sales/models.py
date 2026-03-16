from django.db import models
from django.conf import settings
from products.models import Product

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attendant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    # The price the attendant typed in after bargaining
    negotiated_price = models.BigIntegerField() 
    
    # Auto-calculated field
    total_amount = models.BigIntegerField(editable=False)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Integrity: System calculates total, not the human
        self.total_amount = self.negotiated_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"