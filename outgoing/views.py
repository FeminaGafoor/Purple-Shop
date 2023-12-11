from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem
from products.models import Product
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

# cart view------------------>



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart


def add_cart(request, product_id):
    
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    
    
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
        
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            )
        
        cart_item.save()
    return redirect('outgoing_app:cart')
        
    

def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product = product,cart =cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('outgoing_app:cart') 


def remove_cart_item(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product = product,cart = cart)
    cart_item.delete()
    return redirect('outgoing_app:cart')


    
def cart(request, total=0, quantity=0, cart_items=None):
    shipping = 40  
    tax = 0
    grand_total = 0
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        
        cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('id')

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = (2 * total)/100
            tax = round(tax,2)
            grand_total = total+tax+shipping
            grand_total = round(grand_total, 2)
    except ObjectDoesNotExist:
        pass

    context = {
       
        'quantity': quantity,
        'shipping': shipping,
        'cart_items': cart_items,
        'total': total,
        "tax":tax,
        "grand_total":grand_total,
    }
    return render(request, 'cart.html', context)


