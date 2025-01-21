from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()

def category_image_path(instance, filename):
    return "category/icons/{}/{}".format(instance.name, filename)

def product_image_path(instance, filename):
    return "product/images/{}/{}".format(instance.title, filename)

def product_image_gallery_path(instance, filename):
    return "product/gallery/{}/{}".format(instance.product.title, filename)

def variant_image_path(instance, filename):
    return "product/variations/{}/{}".format(instance.product.title, filename)

class Category(MPTTModel):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to=category_image_path, blank=True)
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = TreeForeignKey(
        Category, related_name="product_category", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    image = models.ImageField(upload_to=product_image_path, blank=True)  # Primary image
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    views = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        return self.title

    


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=product_image_gallery_path)

    def __str__(self):
        return f"Image for {self.product.title}"


class ProductVariation(models.Model):
    product = models.ForeignKey(
        Product, related_name="variations", on_delete=models.CASCADE
    )
    attribute_name = models.CharField(max_length=100)  # e.g., Size, Color
    attribute_value = models.CharField(max_length=100)  # e.g., Medium, Red
    additional_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Price increase for this variation
    barcode = models.CharField(max_length=25)
    image = models.ImageField(upload_to=variant_image_path, blank=True, null=True)  # Variation image
    sku = models.CharField(max_length=25)
    
    bonus_threshold = models.PositiveIntegerField(default=0)  # Nombre nécessaire pour le bonus

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value}"




class PurchaseTracker(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity_purchased = models.PositiveIntegerField(default=0)
    bonus_claimed = models.BooleanField(default=False)


    def check_and_award_bonus(self):
        if not self.bonus_claimed and self.quantity_purchased >= self.variation.bonus_threshold:
            self.bonus_claimed = True
            self.save(update_fields=['bonus_claimed'])
            return True
        return False

    def __str__(self):
        return f"{self.client.username} - {self.variation.attribute_name} - {self.quantity_purchased}"