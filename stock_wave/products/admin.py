# Register your models here.
from django.contrib import admin
from .models import Product
from django.contrib.humanize.templatetags.humanize import intcomma

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Formatting for the Admin list view
    def formatted_cost(self, obj):
        return f"{intcomma(obj.cost_price)} UGX"
    formatted_cost.short_description = "Cost"

    def formatted_selling(self, obj):
        return f"{intcomma(obj.selling_price)} UGX"
    formatted_selling.short_description = "Selling Price"

    # Columns to show in the Admin list
    list_display = ('name', 'quantity', 'formatted_cost', 'formatted_selling', 'created_at')
    
    # Search functionality
    search_fields = ('name', 'description')
    
    # Enable editing quantity directly from the list
    list_editable = ('quantity',)