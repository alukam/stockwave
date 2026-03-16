from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class AttendantRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This loop injects Bootstrap classes into every field automatically
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control', 
                'placeholder': f"Enter {field.label}"
            })

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "phone_number")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_approved = False
        user.role = 'ATTENDANT'
        if commit:
            user.save()
        return user