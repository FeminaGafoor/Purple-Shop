import datetime
from email import message
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from outgoing.models import CartItem
from products.models import ProductVariant
from accounts.models import User_Profile
from django.template.loader import render_to_string
from .models import Order, OrderProduct, Payment
from .forms import OrderForm

# Create your views here.


# def order_place(request):
    
#     cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#     user = request.user
#     user_pro = User_Profile.objects.get(user=user)
    
#     context={
#         'cart_items':cart_items,
#         'user_pro':user_pro
#     }
    
#     return render(request, 'order_place.html',context)
    




def place_order(request, total=0, quantity=0):
    
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
        form = OrderForm(request.POST)
        print("inside form")
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.user_name = form.cleaned_data ['user_name']
            # data.first_name = form.cleaned_data ['first_name']
            # data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']                                                
            data.email = form.cleaned_data['email']
            data.address_1 = form.cleaned_data['address_1']
            data.address_2 = form.cleaned_data['address_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.shipping = shipping
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            
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
            print(form.errors)
            return render(request, 'checkout.html', {'form': form})
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

                # Assuming product_variant is a ForeignKey
                product_variant_instance = item.product_variant.first()  # Assuming you want the first related instance
                if product_variant_instance:
                    order_product.product_variant = product_variant_instance
                    order_product.quantity = item.quantity
                    order_product.price = item.product.price
                    order_product.ordered = True
                    order_product.save()

                    # Update the product_variant quantity
                    product_variant_instance.quantity -= item.quantity
                    product_variant_instance.save()
                
            CartItem.objects.filter(user=request.user).delete()
            
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
                    

    










            
            
def success(request):
    return render(request,'success.html')
    