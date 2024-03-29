

from django.shortcuts import redirect, render

from coupon.models import Coupon
from accounts.models import User_Profile


def coupon(request):
   

    if request.user.is_authenticated:
        user=request.user
  
        user_pro, created = User_Profile.objects.get_or_create(user=user)
        user_profile_image_url = user_pro.image.url if user_pro.image else None
        coupon = Coupon.objects.filter(active=True)
     
        context = {
            'user_profile_image_url': user_profile_image_url,
            'coupon': coupon
        }
        return render(request, "coupon.html", context)
    else:
       
        return render(request, "login_required.html")