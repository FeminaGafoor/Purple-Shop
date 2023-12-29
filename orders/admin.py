from django.contrib import admin
from .models import Order, OrderProduct, Payment

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'price')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'payment', 'order_total', 'status', 'ip', 'created_at')
    list_filter = ('status', 'is_ordered')
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Order, OrderAdmin)


admin.site.register(OrderProduct)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_method', 'amount_paid', 'status', 'created_at')

admin.site.register(Payment, PaymentAdmin)
