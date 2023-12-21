from django.contrib import admin
from . models import Order, OrderProduct, Payment

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'status', 'created_at')
    
admin.site.register(Order,OrderAdmin)




class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'product_variant', 'price')
    
admin.site.register(OrderProduct,OrderProductAdmin)




class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_method', 'amount_paid', 'status', 'created_at')
    
admin.site.register(Payment,PaymentAdmin)