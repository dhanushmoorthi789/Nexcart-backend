from django.contrib import admin
from .models import Category, Product, Review, Favourite
from .models import Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_active']

    list_display = ['name', 'brand', 'sku', 'price', 'discount_price', 'stock', 'is_active']
    search_fields = ['name', 'brand', 'sku']
    fields = ['name', 'description', 'price', 'discount_price', 'brand', 'sku',
          'category', 'image', 'stock', 'is_active']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating']

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
