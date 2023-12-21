from django.shortcuts import get_object_or_404, render
from django.views import View

from outgoing.models import CartItem
from accounts.models import User_Profile
from orders.models import Order, OrderProduct

# Create your views here.



class UserOrderView(View):
    
    template_name="user_order.html"
    
    def get(self,request):    
        
        user_profile = get_object_or_404(User_Profile, user=request.user)
        orders = Order.objects.filter(user=user_profile.user, is_ordered=True).order_by("-created_at")
        order_products = OrderProduct.objects.filter(order__in=orders, user=user_profile).order_by("-id")
        user_profile_image_url = user_profile.image.url if user_profile.image else None
        
        context = {
            "orders": orders,
            "order_products": order_products,
            'user_profile':user_profile,
            'user_profile_image_url':user_profile_image_url
        }

        return render(request,self.template_name,context)



class OrderTrackView(View):
    template_name = "order_track.html"

    def get(self, request, id):
        orders = get_object_or_404(OrderProduct, id=id)
        print(orders.product.product_name,"||||||||||||||||||||||")
        orderstatus = orders.order.status
        print(orderstatus,"ordertrackview user")
        context = {
            "orders": orders,
            "orderstatus":orderstatus,
            }
        return render(request, self.template_name, context)

   