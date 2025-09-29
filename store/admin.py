from django.contrib import admin
from .models import Product, Order, OrderItem, UserProfile, Review, OrderTracking

# ----------------- Product -----------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'original_price', 'rating', 'reviews_count', 'badge')
    list_filter = ('badge',)
    search_fields = ('name', 'description')
    actions = ['mark_as_sale']

    def mark_as_sale(self, request, queryset):
        queryset.update(badge='sale')
        self.message_user(request, f"{queryset.count()} product(s) marked as sale")
    mark_as_sale.short_description = "Mark selected products as Sale"

# ----------------- UserProfile -----------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone')

# ----------------- Order -----------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'phone', 'address', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'full_name', 'phone', 'address', 'id')
    readonly_fields = ('created_at',)
    actions = ['mark_as_cancelled', 'mark_as_shipped', 'mark_as_delivered']

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
        self.message_user(request, f"{queryset.count()} order(s) cancelled")
    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='Shipped')
        self.message_user(request, f"{queryset.count()} order(s) marked as shipped")
    mark_as_shipped.short_description = "Mark selected orders as Shipped"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='Delivered')
        self.message_user(request, f"{queryset.count()} order(s) marked as delivered")
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

# ----------------- OrderItem -----------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'get_total_price')
    list_filter = ('order',)
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('get_total_price',)

    def get_total_price(self, obj):
        return obj.quantity * obj.price
    get_total_price.short_description = "Total Price"




@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__name", "user__username")


@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ("order", "status", "note", "updated_at")
    list_filter = ("status", "updated_at")
    search_fields = ("order__id", "status")