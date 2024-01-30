from django.contrib import admin

from coupon.models import Coupon

# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ('user', 'offer_name' ,'image')

admin.site.register(Coupon,CouponAdmin)