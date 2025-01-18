# order/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, PurchaseTracker

@receiver(post_save, sender=Order)
def update_purchase_tracker(sender, instance, created, **kwargs):
    """
    Signal باش ملي يتسيفا Order جديد (created=True),
    كنزِيدو quantity_purchased ف PurchaseTracker
    ديال داك الكلايان وديك الفارييشن.
    """
    if created:
        # kay9eleb واش كاين PurchaseTracker بقيم client/variation
        # ila ma-kainch, kaycrea wa7ed jdyd
        tracker, _ = PurchaseTracker.objects.get_or_create(
            client=instance.client,
            variation=instance.variation,
        )
        # kanzido f quantity_purchased 9ad quantity dial had l-Order
        tracker.quantity_purchased += instance.quantity
        # kan7afdo
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
