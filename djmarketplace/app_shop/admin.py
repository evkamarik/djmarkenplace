from django.contrib import admin
from .models import Shop, Item, Category, CartItem, Cart


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'name', 'code', 'price', 'stock', 'image']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'customer_name']


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'item_name', 'status']


admin.site.register(Shop, ShopAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)
