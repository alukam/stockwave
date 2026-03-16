from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'ADMIN'
    ATTENDANT = 'ATTENDANT'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (ATTENDANT, 'Store Attendant'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ATTENDANT)
    is_approved = models.BooleanField(default=False)  # Admin must toggle this
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Logic: If it's an Admin, they are auto-approved. 
        # If it's an Attendant, they stay inactive until Admin checks a box.
        if self.role == self.ADMIN:
            self.is_approved = True
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"