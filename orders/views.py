from django.shortcuts import render
from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import datetime
from email import message
import json
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from outgoing.models import CartItem
from products.models import Product, ProductVariant
from accounts.models import PaymentWallet, User_Profile
from django.template.loader import render_to_string
from django.utils import timezone
from coupon.models import Coupon
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
        print(data,"data__________________")
        data.user = current_user
        data.user_name = user_name
        data.phone = phone                                               
        data.email = email
        data.address = address
        data.city = city
        data.state = state
        data.country = country
        data.order_total = grand_total
        data.tax = tax
        data.shipping = shipping
        data.ip = request.META.get('REMOTE_ADDR')
        print(data,"dtaa2__________________")
        data.save()
        print(data,"______________")
        order_id = data.id
        print(order_id,"&&&&&&&&&&&&&&&&&&")
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
        print(order.user_name, order.order_number,order.status, order.phone, order.address, order.city, order.state, order.country)
        print("_________________________________")
        context = {
            'order_id':order_id,
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

    
    print("inside cash on delivery|||||||||||||||||||||||||||||||||")
    if orders.exists():
        order = (
            orders.last()
        ) 
        
        coupon_discount = 0 
        print("if order exist|||||||||||||||||||||||||||||||||")
        if order.coupon:
            coupon_discount = order.coupon.discount_price
            
        payment = Payment(
            user=user_profile,
            payment_id=number,
            payment_method="COD",
            amount_paid=order.order_total - coupon_discount,
            status="Completed",
        )
        print("if no coupon|||||||||||||||||||||||")
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


def apply_coupon(request,total=0, quantity=0):
    if request.method =="POST":
        user=request.user
        cart_items = CartItem.objects.filter(user=user)
        tax = 0
        grand_total = 0
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
           
        tax = (2 * total)/100
        tax = round(tax,2)
        
        shipping = 40 
        grand_total = total+tax+shipping
        grand_total = round(grand_total, 2)
        print(grand_total,"grand_total")
    
        coupon_code = request.POST.get('coupon')
        print(coupon_code,"coupon||||||||")
        coupon = Coupon.objects.filter(code=coupon_code, active=True).first()
        
        
        if coupon:
            current_time=timezone.now()
            if current_time<=coupon.expiration_time:
                
                if Order.objects.filter(user=user, coupon=coupon, is_ordered=True).exists():
                    return JsonResponse({'error': 'You have already used this coupon.'})
                
                orders = Order.objects.filter(user=user,is_ordered=False)
                if orders.exists():
                    order = orders.latest('created_at')
                    
                else:
                    order = Order.objects.create(user=user, total_amount=0)
                    

                # Check if the order total meets the minimum amount requirement
                if total >= coupon.minimum_amount:
                    print(total,"total")
                    print(coupon.discount_price,"coupon.discount_price___________________________")
                    coupon_amount=coupon.discount_price
                    # Apply the discount to the total
                    amount_payable = grand_total - coupon_amount
                    # print(discount_amount,"discount_amount")
                    # amount_payable = grand_total - discount_amount
                    print(amount_payable,"amount_payable+++++++++++++++++++++++++++++++++")
                    order.coupon = coupon
                    order.save()
                    
                    for cart_item in cart_items:
                        cart_item.product.price = grand_total
                    print("inside cart")    
                    response_data = {
                        'total': total,
                        'coupon': coupon_amount,
                        'tax': tax,
                        'shipping': shipping,
                        'grand_total': amount_payable,
                        'success': f"Coupon '{coupon.offer_name}' applied successfully! You saved ₹{coupon.discount_price:.2f}",
                    }
                    return JsonResponse(response_data)
                else:
                    return JsonResponse({'error': f"The order total must be greater than or equal to ₹{coupon.minimum_amount} to use this coupon."})
            else:
                return JsonResponse({'error': 'Invalid coupon or expired'})
        else:
            return JsonResponse({'error': 'Invalid coupon code'})

    return JsonResponse({'error': 'Invalid request method'})

                        


def payments(request):
    body = json.loads(request.body)
    print("from payments||||||||||||||||||||||||||||||||||")
    orders = Order.objects.filter(
        user=request.user, is_ordered=False, order_number=body["orderID"]
    )
    user_profile = get_object_or_404(User_Profile, user=request.user)
    
    if orders.exists():
        order = (
            orders.last()
        ) 
        
        coupon_discount = 0 

        # Check if the order has a coupon applied
        if order.coupon:
            coupon_discount = order.coupon.discount_price
        payment = Payment(
            user=user_profile,
            payment_id=body["transID"],
            payment_method=body["payment_method"],
            amount_paid=order.order_total - coupon_discount,
            status=body["status"],
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
        
        mail_subject = "Thank you for your order"
        message = render_to_string(
            "order_recieved_email.html", {"user": request.user, "order": order}
        )
        to_email = request.user.email

        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.send()

    data = {"order_number": order.order_number, "transID": payment.payment_id}
    return JsonResponse(data)
  


  
    

def order_complete(request):
    order_number = request.GET.get("order_number")
    
    try:
        orders = Order.objects.filter(order_number=order_number, is_ordered=True)
        user_profile = get_object_or_404(User_Profile, user=request.user)
        if orders.exists():
       
            order = orders.last()

            order_products = OrderProduct.objects.filter(order=order, user=user_profile)
            context = {
                    "order_products": order_products,
                }
            return render(request, "success.html",context)
        else:
            # Handle the case where no orders match the criteria
            return HttpResponse("Order not found.")
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return HttpResponseRedirect("/")


def wallet_payment(request, number):
    user_wallet = User_Profile.objects.get(user=request.user)
    orders = Order.objects.filter(user=request.user, is_ordered=False, order_number=number).last()

    if orders and user_wallet.wallet >= orders.order_total:
        coupon_discount = 0 

    #     # Check if the order has a coupon applied
        if orders.coupon:
            coupon_discount = orders.coupon.discount_price

        payment = Payment(
            user=request.user,
            payment_id=number,
            payment_method="Wallet",
            amount_paid=orders.order_total - coupon_discount,
            status="Completed",
        )
        payment.save()

        orders.payment = payment
        orders.is_ordered = True
        orders.save()

        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            order_product = OrderProduct(
                order=orders,
                payment=payment,
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                # variant=item.variant,
                price=item.product.price,
                grand_total = orders.order_total - coupon_discount,
                ordered=True,
            )
            order_product.save()

    #         variant = Variants.objects.get(id=item.variant.id)
    #         variant.quantity -= item.quantity
    #         variant.save()

        order_total_decimal = Decimal(str(orders.order_total))    
        user_wallet.wallet -= order_total_decimal
        user_wallet.save()

        wallet_history = PaymentWallet(
            user=request.user,
            wallet=orders.order_total,
            paymenttype="Debit",
        )
        wallet_history.save()

        cart_items.delete()

    #     # Send order confirmation email
        mail_subject = "Thank you for your order"
        message = render_to_string(
            "order_recieved_email.html", {"user": request.user, "order": orders}
        )
        to_email = request.user.email
        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.send()

        order_products = OrderProduct.objects.filter(order=orders, user=request.user)
        context = {
            "order_products": order_products,
        }
        success_message = "your payment was success"
        return JsonResponse({"success": success_message, "message": success_message})

       
  
    else:
        error_message = "Your wallet balance is insufficient for this transaction."

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"error": error_message, "message": error_message})
        else:
            messages.error(request, error_message)
            return render(request, "payment.html", {"order": orders})





            
            
def success(request):
    order_products = OrderProduct.objects.filter(user=request.user).last()
    context={
        'order_products':order_products
    }
    return render(request,'success.html',context)
    