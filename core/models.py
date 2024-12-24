from django.db import models
from products.models import Product
from user_profile.models import UserProfile

# Create your models here.

class Showcase(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name="showcases", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

    
class UserShowcase(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_showcases')
    showcase = models.ForeignKey(Showcase, on_delete=models.CASCADE, related_name='user_showcases')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'showcase')  # To ensure no duplicate entries

    def __str__(self):
        return f"{self.user.username} - {self.showcase.name}"