from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.list_orders, name='order-list'),
    path('order/<int:order_id>/', views.view_order, name='order-detail'),
    path('order/create/', views.create_order, name='order-create'),
    path('order/update-status/<int:order_id>/', views.update_order_status, name='order-update-status'),
    path('order/delete/<int:order_id>/', views.delete_order, name='order-delete'),
]