from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, default="fa-tag") # For FontAwesome icons

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name