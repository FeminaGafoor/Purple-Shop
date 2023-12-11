from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from outgoing.models import Cart, CartItem
from outgoing.views import _cart_id

from .models import Category, Product

# Create your views here.


# shop view------------------>

def shop(request, category_slug=None):
    total = 0
    quantity = 0
    shipping = 40
    cart_items = None
    categories = None
    product = None

    try:
        if category_slug:
            categories = get_object_or_404(Category, slug=category_slug)
            product = Product.objects.filter(category=categories)
        else:
            product = Product.objects.all().order_by('id')

        # Try to get the Cart object
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax + shipping

            grand_total = round(grand_total, 2)

    except Cart.DoesNotExist:
        # Handle the case where Cart object does not exist
        cart = None
        cart_items = None

    context = {
        'product': product,
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, "shop.html", context)

# single product view------------------>



def single_product(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        
    except Exception as e:
        raise e
    context={
        
        'single_product':single_product,
        
    }
    return render(request, "single_product.html",context)
    
    



    