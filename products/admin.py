from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, ProductImage, ProductVariation,PurchaseTracker

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVariation)
admin.site.register(PurchaseTracker)