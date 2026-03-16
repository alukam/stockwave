from django.db import models
from django.utils import timezone
from django.conf import settings  # <--- 1. Add this import

class AuditSnapshot(models.Model):
    date_generated = models.DateTimeField(default=timezone.now)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    total_debt = models.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    net_cash = models.DecimalField(max_digits=12, decimal_places=2)
    
    # 2. Update this field to use settings.AUTH_USER_MODEL
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True
    )

    def __str__(self):
        return f"Audit {self.date_generated.strftime('%Y-%m-%d')}"