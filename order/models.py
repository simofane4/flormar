
# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from cart.models import Cart

User = get_user_model()

class PaymentMethod(models.TextChoices):
    CASH = 'cash', 'Cash'
    CHECK = 'check', 'Check'

class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    CHECK_PENDING = 'check_pending', 'Check Pending'
    CHECK_CLEARED = 'check_cleared', 'Check Cleared'

class Order(models.Model):
    client = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name="fulfilled_orders", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="order", on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    payment_status = models.CharField(max_length=15, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("confirmed", "Confirmed")], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} for {self.client.username} by {self.seller.username}"

    def is_paid(self):
        if self.payment_method == PaymentMethod.CASH and self.payment_status == PaymentStatus.PAID:
            return True
        elif self.payment_method == PaymentMethod.CHECK and self.payment_status == PaymentStatus.CHECK_CLEARED:
            return True
        return False