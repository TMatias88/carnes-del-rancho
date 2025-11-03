from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order_number", "gateway", "status", "created_at")
    search_fields = ("order_number", "request_id")
    list_filter = ("gateway", "status", "created_at")
