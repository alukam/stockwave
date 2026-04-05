from django.shortcuts import redirect
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views 

# Import your dashboard view specifically
from sales.views import dashboard_view 
from users import views as user_views
from debtors import views as debtor_views

urlpatterns = [
    # Custom Password Reset Routes
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt'
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # 1. Homepage
    path('', dashboard_view, name='dashboard'),

    # 2. System Admin
    path('admin/', admin.site.urls),

    # 3. Authentication
    path('accounts/', include('django.contrib.auth.urls')), 

    # 4. App-specific Included URLs
    path('users/', include('users.urls')),
    path('sales/', include('sales.urls')),
    path('inventory/', include('products.urls')),
    path('expenses/', include('expenses.urls')),
    path('debtors/', include('debtors.urls')),
    path('reports/', include('reports.urls')),

    # 5. Management Routes
    path('management/', user_views.admin_management, name='admin_management'),
    path('management/toggle/<int:user_id>/', user_views.toggle_user_status, name='toggle_user'),
    path('management/delete/<int:user_id>/', user_views.delete_user, name='delete_user'),

    # 6. Payment Route
    path('debtors/payment/<int:debtor_id>/', debtor_views.record_payment, name='record_payment'),
]