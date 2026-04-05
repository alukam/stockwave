from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter parts details...'}),
            # This makes the Boolean look like a toggle in Bootstrap
            'is_fixed_price': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if the product already exists in the DB
        if self.instance and self.instance.pk:
            self.fields['quantity'].disabled = True
            self.fields['quantity'].help_text = "Stock quantity cannot be edited. Please use the 'Restock' feature to add inventory."