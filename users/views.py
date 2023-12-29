from django.shortcuts import get_object_or_404, render
from django.views import View
from django.contrib import messages
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
        
        
        for order_product in order_products:
            try:
                # Assuming you want to get the CartItem related to the OrderProduct
                cart_item = CartItem.objects.get(id=order_product.product.id)
                product_variations = cart_item.product_variant.all()
                # Assuming you have a field named 'product_variants' in your OrderProduct model
                order_product.product_variant.set(product_variations)
            except CartItem.DoesNotExist:
                # Handle the case where the CartItem does not exist
                pass
        
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
        
        orderstatus = orders.order.status
        
        context = {
            "orders": orders,
            "orderstatus":orderstatus,
            }
        return render(request, self.template_name, context)



class CancelOrder(View):

    template_name = "track_order.html" 

    def post(self, request, id):
        if request.method == 'POST':
            reason = request.POST.get('cancel_reason')
            if not reason:
                messages.error(request,"Cancel reason is required.")
                return render(request, self.template_name)
                
            orders = get_object_or_404(OrderProduct, id=id)
            orders.user_note = reason
            orders.status = "Canceled"
            orders.save()
            return render(request, self.template_name)
    
   