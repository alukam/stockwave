from django.shortcuts import redirect
from django.urls import path, include
from django.contrib import admin
# Import your dashboard view specifically
from sales.views import dashboard_view 

urlpatterns = [
    # 1. THE WINNER: This is your homepage now.
    path('', dashboard_view, name='dashboard'),

    # 2. System Admin
    path('admin/', admin.site.urls),

    # 3. Authentication (Login/Logout)
    path('accounts/', include('django.contrib.auth.urls')), 

    # 4. App-specific URLs
    path('users/', include('users.urls')),
    path('sales/', include('sales.urls')),
    path('inventory/', include('products.urls')),
    path('expenses/', include('expenses.urls')),
    path('debtors/', include('debtors.urls')),
    path('reports/', include('reports.urls')),
    
    # REMOVED: The lambda redirect at the bottom. 
    # Since path('') is already taken by the dashboard, the lambda will never run.
]