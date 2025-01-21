from django.db import models
from django.contrib.auth import get_user_model
from products.models import ProductVariation

User = get_user_model()

class Cart(models.Model):
    client = models.OneToOneField(User, related_name="carts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.client.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_variation.product.title} in {self.cart.client.username}'s cart"

