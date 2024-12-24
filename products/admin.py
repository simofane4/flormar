from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, ProductImage, ProductVariation

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVariation)