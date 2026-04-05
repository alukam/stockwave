from django.urls import path
from . import views

urlpatterns = [
    # This is your main sales table (127.0.0.1:8000/sales/)
    path('', views.sales_management, name='sales_management'), 
    
    # Adding a new sale
    path('add/', views.create_sale, name='add_sale'),
    
    # Editing an existing sale
    path('edit/<int:sale_id>/', views.edit_sale, name='edit_sale'),
    
    # Cancelling a sale
    path('cancel/<int:sale_id>/', views.cancel_sale, name='cancel_sale'),
]