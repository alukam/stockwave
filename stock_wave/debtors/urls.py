from django.urls import path
from . import views

urlpatterns = [
    path('', views.debtor_list, name='debtor_list'),
    path('add/', views.add_debtor, name='add_debtor'),
    path('<int:debtor_id>/', views.debtor_detail, name='debtor_detail'),
    path('payment/edit/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('payment/delete/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('edit/<int:debtor_id>/', views.edit_debtor, name='edit_debtor'),
    path('delete/<int:debtor_id>/', views.delete_debtor, name='delete_debtor'),
]