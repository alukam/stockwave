from django.urls import path
from . import views

# This list MUST be named exactly 'urlpatterns'
urlpatterns = [
    path('', views.product_list, name='inventory'),
    path('add/', views.add_product, name='add_product'),
]