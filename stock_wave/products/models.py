from django.db import models
from categories.models import Category # Ensure the categories app is created first

class Product(models.Model):
    # 1. Name (How the product is known in the shop)
    name = models.CharField(
        max_length=255, 
        verbose_name="How the product is known in the shop"
    )

    # 2. Categories (Drop down and select an option)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='products',
        verbose_name="Category"
    )

    # 3. Cost in UGX
    cost_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Cost in UGX"
    )

    # 4. Price (Price at which the product is sold to the customer)
    selling_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Price (Sold to Customer)"
    )

    # 5. Quantity (Current stock)
    quantity = models.PositiveIntegerField(
        default=0, 
        verbose_name="Current Stock"
    )

    # 6. Location (Within the shop)
    location = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Location within the shop"
    )

    # 7. Made in (Origin of the product)
    origin = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Made in (Origin)"
    )

    # 8. Description (With text editor features)
    # Note: Use TextField here; we will hook up the Rich Text Editor in the Form/Admin
    description = models.TextField(
        blank=True, 
        verbose_name="Product Description"
    )

    # 9. Photo
    photo = models.ImageField(
        upload_to='product_photos/', 
        blank=True, 
        null=True, 
        verbose_name="Product Photo"
    )

    # 10. Toggle button (Changing price)
    # Label: Goods and products without fixed price
    has_fixed_price = models.BooleanField(
        default=True, 
        verbose_name="Goods and products without fixed price"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name