import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render

from outgoing.models import CartItem

from .models import Order, OrderProduct
from .forms import OrderForm

# Create your views here.

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
            
            
            return render(request,'payment.html',context)
        else:
            print(form.errors)
            return render(request, 'checkout.html', {'form': form})
    else:
        return redirect('outgoing_app:checkout')
            
            
            
            
def payment(request):
    # current_user = request.user
    # orders = Order.objects.filter(user=current_user, is_ordered=False)
    # print(orders, "order_user")
    # if orders.exists():
    #     order = (
    #         orders.last()
    #     )
        
    #     cart_item = CartItem.objects.filter(user=request.user)
    #     for item in cart_item:
    #         orderproduct = OrderProduct()
    #         orderproduct.order = order
    #         # orderproduct.payment = payment
    #         # orderproduct.user = request.user
    #         # orderproduct.product = item.product
    #         # orderproduct.quantity = item.quantity
    #         # orderproduct.variant = item.variant
    #         # orderproduct.price = item.variant.price
    #         # orderproduct.ordered = True
    #         # orderproduct.save()

    #         # variant = Variants.objects.get(id=item.variant.id)
    #         # variant.quantity -= item.quantity
    #         # variant.save()
    # context = {
    #     'orders': orders
    # }
    return render(request, 'payment.html')