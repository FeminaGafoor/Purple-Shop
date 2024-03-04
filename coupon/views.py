

from django.shortcuts import redirect, render

from coupon.models import Coupon
from accounts.models import User_Profile


def coupon(request):
   

    if request.user.is_authenticated:
        user=request.user
        print("from coupon@@@@@@@@@@@@@@@@@@@@@@@@")
        user_pro, created = User_Profile.objects.get_or_create(user=user)
        user_profile_image_url = user_pro.image.url if user_pro.image else None
        coupon = Coupon.objects.filter(active=True)
        print(coupon,"coupon!!!!!!!!!!!!!!!")
        context = {
            'user_profile_image_url': user_profile_image_url,
            'coupon': coupon
        }
        return render(request, "coupon.html", context)
    else:
        # Handle the case where the user is not authenticated
        return render(request, "login_required.html")