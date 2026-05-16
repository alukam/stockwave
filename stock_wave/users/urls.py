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

    path('login/', views.IMSLoginView.as_view(), name='login'),
    # ... your other paths ...

    # 1. The page the user sees to enter their email
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html'
    ), name='password_reset'),

    # 2. The "Success! Check your email" page
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    # 3. The link from the email (This is the one your email template is looking for!)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # 4. The "Password successfully changed" page
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]