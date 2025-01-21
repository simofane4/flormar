# order/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models import CartItem
from .models import Order
from products.models import ProductVariation, PurchaseTracker

@receiver(post_save, sender=Order)
def update_purchase_tracker(sender, instance, created, **kwargs):
    if created:
        # Get all CartItems from the cart
        cart_items = CartItem.objects.filter(cart=instance.cart)

        for cart_item in cart_items:
            variation = cart_item.product_variation  # Get the ProductVariation
            
            # Create or update the tracker for each variation
            tracker, _ = PurchaseTracker.objects.get_or_create(
                client=instance.client,
                variation=variation,
            )
            
            # Update the quantity purchased
            tracker.quantity_purchased += cart_item.quantity
            tracker.save()


@receiver(post_save, sender=PurchaseTracker)
def award_bonus_after_purchase(sender, instance, created, **kwargs):
    """
    Signal باش ملي يتسيفا PurchaseTracker (jadid ou update),
    كنعيطو ل check_and_award_bonus باش نشوفو واش
    bonus_threshold وصل ولا مازال.
    """
    # ila bghiti tkhdem ghir mra l-awla d creation => if created:
    instance.check_and_award_bonus()
