from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('login/', views.IMSLoginView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
       # email_template_name='users/password_reset_email.html'
    ), name='password_reset'),
    
    # Management
    path('management/', views.admin_management, name='admin_management'),
    path('management/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user'),
    path('management/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]