from django.contrib import admin

from models import Product

@admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_filter = ['name', 'price']
    search_fields = ['category', 'name']
    fields = (
        ['name', 'price'],
        ['category', 'name']
    )