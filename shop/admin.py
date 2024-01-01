from django.contrib import admin
from .models import *

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_status')
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def stock_status(self, obj):
        if obj.stock == 'in stock':
            return 'In Stock'
        elif obj.stock == 'low stock':
            return 'Low Stock'
        else:
            return 'Out of Stock'

    stock_status.short_description = 'Stock Status'

@admin.register(Redeem)
class RedeemAdmin(admin.ModelAdmin):
   list_display = ('code', 'diamonds', 'redeemed')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'x_coordinate', 'z_coordinate', 'cart_total', 'date_delivery')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'auth_token', 'is_verified', 'created_at', 'balance')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'price', 'subtotal')