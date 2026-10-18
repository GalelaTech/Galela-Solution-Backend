from django.contrib import admin
from .models import ServiceCategory, ServiceOption


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'display_order', 'is_active', 'updated_at']
    list_editable = ['display_order', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}   # auto-fills slug from name
    ordering = ['display_order', 'name']


@admin.register(ServiceOption)
class ServiceOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'display_order', 'is_active', 'updated_at']
    list_editable = ['display_order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    autocomplete_fields = ['category']
    ordering = ['category', 'display_order', 'name']