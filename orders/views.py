import datetime
from email import message
import json
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from outgoing.models import CartItem
from products.models import Product, ProductVariant
from accounts.models import User_Profile
from django.template.loader import render_to_string
from .models import Order, OrderProduct, Payment


# Create your views here.






def place_order(request, total=0, quantity=0):
    
    print("+++++++++++++++++++placeor")
    current_user = request.user
    # if the cart count <= 0 redirect to shop
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('shop_app:shop')
    
    
    
    grand_total = 0
    shipping = 40  
    tax = 0
    
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    tax = round(tax,2)
    grand_total = total+tax+shipping
    grand_total = round(grand_total, 2)
    
    if request.method == "POST":
        # form = OrderForm(request.POST)
        print("inside form")
        user_name = request.POST.get("user_name")
        print(user_name,"user_name000000000")
        phone = request.POST.get("phone")
        print(phone,"phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        if (
            not user_name
            or not phone
            or not email
            or not address
            or not state
            or not city
            or not country
        ):
            print("++++++++++++++++++++")
            messages.error(request, "Please fill in all required fields.")
            return redirect("order_app:place_order/")

            
        print("___________________________")
        data = Order()
        data.user = current_user
        data.user_name = user_name
        data.phone = phone                                               
        data.email = email
        data.address_1 = address
        data.city = city
        data.state = state
        data.country = country
        data.order_total = grand_total
        data.tax = tax
        data.shipping = shipping
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        print(data,"______________")
        
        
        # generate order number
        
        yr = int(datetime.date.today().strftime('%Y'))  # Use %Y instead of %y
        mt = int(datetime.date.today().strftime('%m'))
        dt = int(datetime.date.today().strftime('%d'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()
        
        
        
        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
        print(order.user_name, order.order_number, order.phone, order.address_1, order.city, order.state, order.country)
        print("_________________________________")
        context = {
            'order':order,
            'cart_items': cart_items,
            'total':total,
            'tax':tax,
            'shipping':shipping,
            'grand_total': grand_total
        }
        
        
        return render(request,'place_order.html',context)
    else:
        return redirect('outgoing_app:checkout')
                

            
def cash_on_delivery(request,number):
    
    orders = Order.objects.filter(user=request.user, 
                                  is_ordered=False, order_number=number)
    
    user_profile = get_object_or_404(User_Profile, user=request.user)

    
    
    if orders.exists():
        order = (
            orders.last()
        ) 
        
       
        
        if order:
            payment = Payment(
                user=user_profile,
                payment_id=number,
                payment_method="COD",
                amount_paid=order.order_total, 
                status="Completed",
            )
            
            payment.save()
            order.payment = payment
            order.is_ordered = True
            order.save()
            
            cart_item = CartItem.objects.filter(user=request.user)
            
            for item in cart_item:
                order_product = OrderProduct()
                order_product.order = order
                order_product.payment = payment
                order_product.user = user_profile
                order_product.product = item.product
                order_product.price = item.product.price
                order_product.quantity = item.quantity
                order_product.save()
                
                
                cart_item = CartItem.objects.get(id=item.id)
                product_variation = cart_item.product_variant.all()
                order_product = OrderProduct.objects.get(id=order_product.id)
                order_product.product_variant.set((product_variation))
                order_product.save()

                # Reduce the quantity of sold product
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()
                
                
            # Clear cart    
            CartItem.objects.filter(user=request.user).delete()
            
            
            # order recieved email
            mail_subject = "Thank you for your order"
            message = render_to_string(
                "order_recieved_email.html", {"user": request.user, "order": order}
            )
            to_email = request.user.email

            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()
            
            order_products = OrderProduct.objects.filter(order=order, user=user_profile)
            
            context = {
                    "order_products": order_products,
                }
            return render(request, "success.html",context)
        else:
            return HttpResponseRedirect('/')
                    

            
def payments(request,number):
    body = json.loads(request.body)
    orders = Order.objects.filter(user=request.user, 
                                  is_ordered=False, order_number=number)
    user_profile = get_object_or_404(User_Profile, user=request.user)
    if orders.exists():
        order = (
            orders.last()
        ) 
        
       
        
        if order:
            payment = Payment(
                user=user_profile,
                payment_id=number,
                payment_method="COD",
                amount_paid=order.order_total, 
                status="Completed",
            )
            
            payment.save()
            order.payment = payment
            order.is_ordered = True
            order.save()
            
            cart_item = CartItem.objects.filter(user=request.user)
            
            for item in cart_item:
                order_product = OrderProduct()
                order_product.order = order
                order_product.payment = payment
                order_product.user = user_profile
                order_product.product = item.product
                order_product.price = item.product.price
                order_product.quantity = item.quantity
                order_product.save()
                
                
                cart_item = CartItem.objects.get(id=item.id)
                product_variation = cart_item.product_variant.all()
                order_product = OrderProduct.objects.get(id=order_product.id)
                order_product.product_variant.set((product_variation))
                order_product.save()

                # Reduce the quantity of sold product
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()
                
                
            # Clear cart    
            CartItem.objects.filter(user=request.user).delete()
            
            
            # order recieved email
            mail_subject = "Thank you for your order"
            message = render_to_string(
                "order_recieved_email.html", {"user": request.user, "order": order}
            )
            to_email = request.user.email

            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()

        data = {"order_number": order.order_number, "transID": payment.payment_id}
        return JsonResponse(data)
    else:
        # Handle the case when no matching order is found
        return HttpResponse("Order not found.")


def order_complete(request):
    order_number = request.GET.get("order_number")
    
    try:
        orders = Order.objects.filter(order_number=order_number, is_ordered=True)

        if orders.exists():
       
            order = orders.last()

            order_products = OrderProduct.objects.filter(order=order, user=request.user)
            context = {
                    "order_products": order_products,
                }
            return render(request, "success.html",context)
        else:
            # Handle the case where no orders match the criteria
            return HttpResponse("Order not found.")
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return HttpResponseRedirect("/")






            
            
def success(request):
    return render(request,'success.html')
    