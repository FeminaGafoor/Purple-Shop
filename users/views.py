from django.utils import timezone
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
        
        sub_total = 0
        for order_product in order_products:
            # Calculate the subtotal for each ordered product
            product_subtotal = order_product.price * order_product.quantity
            sub_total += product_subtotal
            tax = (2 * product_subtotal)/100

        # Add additional charges (tax, shipping, etc.) to the subtotal
        additional_charges = 40 + tax # Example: You can replace this with your actual additional charges
        total = sub_total + additional_charges
            
        
        
        context = {
            "orders": orders,
            "order_products": order_products,
            'sub_total': sub_total,
            'total': total,
            'user_profile':user_profile,
            'user_profile_image_url':user_profile_image_url
        }

        return render(request,self.template_name,context)



class OrderTrackView(View):
    template_name = "order_track.html"

    def get(self, request, id):
        order_detail = get_object_or_404(OrderProduct, id=id)
        print(order_detail,"order_detail+++++++++++++++++")
        
        orderstatus = order_detail.order.status
        print(orderstatus,"orderstatus+++++++++++++++++")
        accepted_timestamp = order_detail.updated_at if order_detail.updated_at else order_detail.create_at
        seven_days_ago = accepted_timestamp + timezone.timedelta(days=7)
        time = timezone.now()
        context = {
            "order_detail": order_detail,
            "orderstatus":orderstatus,
            "seven":seven_days_ago,
            "time":time,
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
    
#    class OrderReturn(View):
    
#     def post(self, request, id):
#         url = request.META.get('HTTP_REFERER')
#         if request.method == 'POST':
#             reason = request.POST.get('return_reason')
#             if not reason:
#                 messages.error(request,"return reason is required.")
#                 return HttpResponseRedirect(url)
#             order_product = get_object_or_404(OrderProduct, id=id)
#             # Check if the order was placed within the last 7 days since status became "Accepted"
#             accepted_timestamp = order_product.update_at if order_product.update_at else order_product.create_at
#             seven_days_ago = accepted_timestamp + timezone.timedelta(days=7)
#             time = timezone.now()
#             if time > seven_days_ago:
#                 messages.error(request, "You can only return the order within 7 days after it's accepted.")
                
#                 return HttpResponseRedirect(url)
#             else:   
#                 orders = get_object_or_404(OrderProduct, id=id)
#                 orders.user_note = reason
#                 orders.status = "Return"
#                 orders.save()
#                 return HttpResponseRedirect(url)
