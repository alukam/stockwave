from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('delete/<int:category_id>/', views.delete_category, name='delete_category'),
]