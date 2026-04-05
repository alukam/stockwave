from django.contrib import admin
from .models import Product
from django.contrib.humanize.templatetags.humanize import intcomma


from django.contrib import admin
from .models import Product
from django.contrib.humanize.templatetags.humanize import intcomma

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 1. Define the methods FIRST inside the class
    def formatted_cost(self, obj):
        return f"{intcomma(int(obj.cost_price))} UGX"
    formatted_cost.short_description = "Cost (UGX)"

    def formatted_selling(self, obj):
        return f"{intcomma(int(obj.selling_price))} UGX"
    formatted_selling.short_description = "Selling Price"

    # 2. Now reference them in list_display
    list_display = ('name', 'category', 'quantity', 'formatted_cost', 'formatted_selling', 'location', 'origin')
    
    # 3. TEMPORARILY comment these out to let the migration pass
    # list_filter = ('category', 'origin', 'is_fixed_price')
    search_fields = ('name', 'description', 'location')
    # readonly_fields = ('created_at', 'updated_at')

    # 4. Simplify fieldsets for the initial migration
    fieldsets = (
        ("Shop Identity", {
            'fields': ('name', 'category', 'location', 'origin')
        }),
        ("Financials & Stock", {
            # Removed 'is_fixed_price' until migration is done
            'fields': ('cost_price', 'selling_price', 'quantity'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('quantity',)
        return self.readonly_fields