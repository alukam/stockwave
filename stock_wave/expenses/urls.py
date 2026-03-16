from django.urls import path
from . import views
urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('cancel/<int:expense_id>/', views.cancel_expense, name='cancel_expense'),
]