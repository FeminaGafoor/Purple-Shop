from django.shortcuts import render

from outgoing.models import CartItem
from accounts.models import User_Profile

# Create your views here.




def user_order(request):
    
    
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user, is_active=True)
    
    user_pro = User_Profile.objects.get(user=current_user)
    user_profile_image_url = user_pro.image.url if user_pro.image else None
    
    context={
        'cart_items':cart_items,
        'user_pro':user_pro,
        'user_profile_image_url':user_profile_image_url
}
    return render(request,'user_order.html',context)


def order_track(request):
    return render(request,'order_track.html')