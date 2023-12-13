from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem
from products.models import Product, ProductVariant
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
    product_variants = []
    if request.method=="POST":
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variants = ProductVariant.objects.get(product= product,variant_types=key, variant_value=value)
                product_variants.append(variants)
         
            except:
                pass
        
    
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    
    is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product,cart=cart)
       
        # existing variations --> database
        # current variantions ---> product_variants = []
        # item_id ---> database
        ex_var_list=[]
        id = []
        for item in cart_item:
            
            existing_variation = item.product_variant.all()
            
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
            
        
        
        if product_variants in ex_var_list:
            # increase cart_item quantity
            index = ex_var_list.index(product_variants)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity +=1
            item.save()
            
        else:
            # create a new cart item
            item = CartItem.objects.create(product = product, quantity =1, cart=cart)
            if len(product_variants)>0:
                item.product_variant.clear()
                item.product_variant.add(*product_variants)
            item.save()
        
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            )
        
        if len(product_variants)>0:
            cart_item.product_variant.clear()
            cart_item.product_variant.add(*product_variants)
        
        cart_item.save()
    return redirect('outgoing_app:cart')
        
    

def remove_cart(request,product_id,cart_item_id ):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product = product,cart =cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('outgoing_app:cart') 


def remove_cart_item(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product = product,cart = cart,id=cart_item_id)
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


def checkout(request):
    return render(request, 'checkout.html')
