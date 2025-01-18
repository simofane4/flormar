from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, User

class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    SELLER = 'seller', 'Seller'
    CLIENT = 'client', 'Client'

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserProfile(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CLIENT,  # Default role is 'client'
    )
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # New field
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Le pourcentage de remise pour le client."
    )
    assigned_seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="clients", null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, related_name="residents", null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_profiles", null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="updated_profiles", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username or self.phone_number or 'No username or phone number'
