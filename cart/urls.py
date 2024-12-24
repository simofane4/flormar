# urls.py
from django.urls import path
from .views import CartView, AddCartItemView, UpdateCartItemView, RemoveCartItemView, ClearCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart-view'),  # View the cart
    path('cart/add/', AddCartItemView.as_view(), name='add-to-cart'),  # Add item to cart
    path('cart/update/', UpdateCartItemView.as_view(), name='update-cart-item'),  # Update item quantity
    path('cart/remove/', RemoveCartItemView.as_view(), name='remove-from-cart'),  # Remove item from cart
    path('cart/clear/', ClearCartView.as_view(), name='clear-cart'),  # Clear the cart
]
