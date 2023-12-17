import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render

from outgoing.models import CartItem
from .models import Order
from .forms import OrderForm

# Create your views here.

def place_order(request, total=0, quantity=0):
    print("|||||||||||||||||||||")
    current_user = request.user
    print(current_user,"|||||||||||||||||||||||||||||")
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
            return redirect('order_app:payment')
        else:
            print(form.errors)
            return render(request, 'checkout.html', {'form': form})
    else:
        return redirect('outgoing_app:checkout')
            
            
            
            
def payment(request):
    return HttpResponse("haiii")