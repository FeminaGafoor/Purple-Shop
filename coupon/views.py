

from django.shortcuts import redirect, render

from coupon.models import Coupon


def coupon(request):
    
    coupon= Coupon.objects.all()
    
    context={
        "coupon":coupon
    }
    return render(request, "coupon.html", context)