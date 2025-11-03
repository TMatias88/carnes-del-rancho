from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "qty", "price_crc", "total_crc")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "name", "total_crc", "payment_method")
    list_filter = ("payment_method", "created_at")
    search_fields = ("name", "email", "phone")
    inlines = [OrderItemInline]
