from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("subtotal",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "full_name", "total", "status", "payment_status", "created_at")
    list_filter = ("status", "payment_status")
    search_fields = ("order_number", "full_name", "email")
    inlines = [OrderItemInline]
    readonly_fields = ("order_number", "created_at", "updated_at")


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "uses", "max_uses", "is_active")
