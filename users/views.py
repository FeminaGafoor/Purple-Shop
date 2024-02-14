from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from outgoing.models import CartItem
from accounts.models import User_Profile
from orders.models import Order, OrderProduct

# Create your views here.



# class UserOrderView(View):
    
#     template_name="user_order.html"
    
#     def get(self,request):    
        
#         user_profile = get_object_or_404(User_Profile, user=request.user)
#         orders = Order.objects.filter(user=user_profile.user, is_ordered=True).order_by("-created_at")
#         order_products = OrderProduct.objects.filter(order__in=orders, user=user_profile).order_by("-id")
#         user_profile_image_url = user_profile.image.url if user_profile.image else None
        
#         sub_total = 0
#         for order_product in order_products:
#             # Calculate the subtotal for each ordered product
#             product_total = order_product.price * order_product.quantity
#             sub_total += product_total
#             tax = (2 * product_total)/100

#         # Add additional charges (tax, shipping, etc.) to the subtotal
#         additional_charges = 40 + tax # Example: You can replace this with your actual additional charges
#         grand_total = sub_total + additional_charges
            
        
        
#         context = {
#             "orders": orders,
#             "order_products": order_products,
#             'sub_total': sub_total,
#             'grand_total': grand_total,
#             'user_profile':user_profile,
#             'user_profile_image_url':user_profile_image_url
#         }

#         return render(request,self.template_name,context)


class UserOrderView(View):
    template_name = "user_order.html"

    def get(self, request):
        user_profile = get_object_or_404(User_Profile, user=request.user)
        orders = Order.objects.filter(user=user_profile.user, is_ordered=True).order_by("-created_at")
        user_profile_image_url = user_profile.image.url if user_profile.image else None
        
        print("order_detail||||||||||||||")
        order_data = []  # List to store order details and associated products
        
        for order in orders:
            order_products = OrderProduct.objects.filter(order=order, user=user_profile).order_by("-id")
            
            sub_total = 0
            for order_product in order_products:
                product_total = order_product.price * order_product.quantity
                sub_total += product_total
                tax = (2 * sub_total) / 100
                
                coupon_discount = order.coupon.discount_price if order.coupon else 0
                
            additional_charges = 40 + tax
            grand_total = sub_total + additional_charges-coupon_discount
            
            order_data.append({
                'order': order,
                'order_products': order_products,
                'sub_total': sub_total,
                'grand_total': grand_total,
                'user_profile':user_profile,
                'user_profile_image_url':user_profile_image_url,
                'order_id': order.id,  # Ensure that you have the correct attribute for the order ID
            })

        context = {
            
            "order_data": order_data,
            'user_profile': user_profile,
            'user_profile_image_url': user_profile_image_url
        }

        return render(request, self.template_name, context)
    
    
    
    

class OrderTrackView(View):
    template_name = "order_track.html"

    def get(self, request, id):
        order_detail = get_object_or_404(OrderProduct, id=id)
        
        
        orderstatus = order_detail.order.status
       
        accepted_timestamp = order_detail.updated_at if order_detail.updated_at else order_detail.created_at
        
        seven_days_ago = accepted_timestamp + timezone.timedelta(days=7)
        
        time = timezone.now()
        context = {
            "order_detail": order_detail,
            "orderstatus":orderstatus,
            "seven":seven_days_ago,
            "time":time,
            }
        return render(request, self.template_name, context)




#Cancel order                 
class CancelOrder(View):
    
    template_name = 'order_track.html'

    def post(self, request, id):
        print("||||||||||||||halooooooooooooooo")
        url = request.META.get("HTTP_REFERER")
        if request.method == 'POST':
            reason = request.POST.get('cancel_reason')
            if not reason:
                messages.error(request, "Cancel reason is required.")
                return redirect(url)

            orders = get_object_or_404(OrderProduct, id=id)
            orders.user_note = reason
            orders.status = "Cancelled"
            orders.save()

            return redirect(url)

# class CancelOrder(View):
#     print("from cancel order|||||||||||||")
#     template_name = "order_track.html" 

#     def post(self, request, id):
        
#         if request.method == 'POST':
#             reason = request.POST.get('cancel_reason')
            
#             if not reason:
                
#                 messages.error(request,"Cancel reason is required.")
#                 return render(request, self.template_name)
#             else:
                
#                 order_detail = get_object_or_404(OrderProduct, id=id)
                
#                 print(order_detail.id,"order_detail.id")
#                 order_detail.user_note = reason
#                 order_detail.status = "Cancelled"
#                 print(order_detail.status,"order_detail.status")
#                 order_detail.save()
                
#                 return render(request, self.template_name)
    

    

class Invoice(View):
    template_name = "user_invoice.html"

    def get(self, request, id):
        user_profile = get_object_or_404(User_Profile, user=request.user)
        order = get_object_or_404(Order, id=id, user=user_profile.user)
        print(order.user,"order||||||||||||||||||||||||")
        order_products = OrderProduct.objects.filter(order=order, user=user_profile).order_by("-id")
        print(order_products,"order_products||||||||||||||")
        
        subtotal = sum(order_product.price * order_product.quantity for order_product in order_products)
        tax = (2 * subtotal) / 100
        shipping = 40
        coupon_discount = order.coupon.discount_price if order.coupon else 0
        grand_total = subtotal + tax + shipping - coupon_discount

        context = {
            'order': order,
            'order_products': order_products,
            'subtotal': subtotal,
            'tax': tax,
            'shipping': shipping,
            'coupon_discount': coupon_discount,
            'grand_total': grand_total,
        }

        return render(request, self.template_name, context)

    
    
    
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
