from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    # Basic Identification
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, help_text="e.g. Car models, brand, or shelf location")
    
    # Inventory
    quantity = models.PositiveIntegerField(default=0)
    
    # Pricing (UGX)
    cost_price = models.BigIntegerField(validators=[MinValueValidator(0)])
    selling_price = models.BigIntegerField(validators=[MinValueValidator(0)])
    min_price = models.BigIntegerField(help_text="The absolute lowest price for bargaining")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name