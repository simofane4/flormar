from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('update-payment-status/<int:order_id>/', views.update_payment_status, name='update-payment-status'),
]