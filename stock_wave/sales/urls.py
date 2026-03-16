from django.urls import path
from . import views

# Django MUST see this exact variable name: urlpatterns
urlpatterns = [
    # 127.0.0.1:8000/sales/
    path('', views.sales_list, name='sales_list'), 
    
    # 127.0.0.1:8000/sales/add/
    path('add/', views.create_sale, name='add_sale'),
    path('cancel/<int:sale_id>/', views.cancel_sale, name='cancel_sale'),
    
]