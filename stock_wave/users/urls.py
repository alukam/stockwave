# users/urls.py
from django.urls import path
from . import views  # Import the whole views module
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.IMSLoginView.as_view(), name='login'), # Use views.Name
    path('register/', views.register_view, name='register'),   # Use views.Name
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]