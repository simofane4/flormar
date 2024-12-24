# admin.py
from django.contrib import admin
from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

# Customizing Cart Item Admin View
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # Don't display extra empty rows

# Customizing Cart Admin View
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('client', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('client__username', 'client__phone_number')
    inlines = [CartItemInline]  # Display cart items inline within the Cart admin

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('items')  # Prefetch related items for better performance

# Customizing Cart Item Admin View
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart__client', 'product')
    search_fields = ('product__title', 'cart__client__username')