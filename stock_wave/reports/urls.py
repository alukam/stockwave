from django.urls import path
from . import views

urlpatterns = [
    path('audit/', views.business_audit_view, name='audit_report'),
    
    # We can add more reports here later (e.g., tax, inventory logs)
]