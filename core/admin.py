from django.contrib import admin

from core.models import Showcase, UserShowcase

# Register your models here.


@admin.register(Showcase)
class ShowcaseAdmin(admin.ModelAdmin):
    list_display = ['name',  'created_at']
    search_fields = ['name']
    filter_horizontal = ['products'] 

@admin.register(UserShowcase)
class UserShowcaseAdmin(admin.ModelAdmin):
    list_display = ['user','showcase', 'created_at']
    search_fields = ['user']
    