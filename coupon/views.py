from django.shortcuts import render
from accounts.models import User_Profile

from coupon.models import Coupon

# Create your views here.
    
def coupon(request):
    
    coupon = Coupon.objects.filter(active=True) 
    profile = User_Profile.objects.get(user=request.user)
    user_profile_image_url = profile.image.url if profile.image else None
    
    
    context = {
        'profile': profile,
        'coupon': coupon,
        'user_profile_image_url':user_profile_image_url,
    }
    return render(request,"coupon.html",context)   