from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import User_Profile
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
    current_user=request.user
    product = Product.objects.get(id=product_id) # get the product
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variants = []
        if request.method=="POST":
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variants = ProductVariant.objects.get(product= product,variant_types__iexact=key, variant_value__iexact=value)
                    product_variants.append(variants)
                    print(variants,"variants_______________________________________")
                    print(product_variants,"variants++++++++++++++++++++++++++++++++++++++")
                except:
                    pass
            
      

        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product,user=current_user)
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
                item = CartItem.objects.create(product = product, quantity =1, user=current_user)
                if len(product_variants)>0:
                    item.product_variant.clear()
                    item.product_variant.add(*product_variants)
                item.save()
            
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
                )
            
            if len(product_variants)>0:
                cart_item.product_variant.clear()
                cart_item.product_variant.add(*product_variants)
            
            cart_item.save()
        return redirect('outgoing_app:cart')
        
        
        
        
    # if the user is not authenticated 
    else:
        product_variants = []
        if request.method=="POST":
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    
                    variants = ProductVariant.objects.get(product= product,variant_types__iexact=key, variant_value__iexact=value)
                    product_variants.append(variants)
                    print(variants,"variants|||||||||||||||||||||||||||||")
                    print(product_variants,"product_variants|||||||||||||||||||||||||||||||||")
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
            # current variations ---> product_variants = []
            # item_id ---> database
            ex_var_list=[]
            id = []
            for item in cart_item:
                
                existing_variation = item.product_variant.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list,"+++++++++++++++++++++++++++++++++++++++++++++++++++")   
            
            
            if product_variants in ex_var_list:
                print("@@@@@@@@@@@@@@")
                # increase cart_item quantity
                index = ex_var_list.index(product_variants)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity +=1
                item.save()
                
            else:
                # create a new cart_item
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
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product = product,user = request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
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
    
    product = get_object_or_404(Product,id = product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product = product,user = request.user ,id=cart_item_id)
    else:
        
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product = product,cart = cart,id=cart_item_id)
    cart_item.delete()
    referring_page = request.META.get('HTTP_REFERER')
    return redirect(referring_page)


    
def cart(request, total=0, quantity=0, cart_items=None):
    shipping = 40  
    tax = 0
    grand_total = 0

    try:
        if request.user.is_authenticated:
           
           cart_items = CartItem.objects.filter(user=request.user, is_active=True)
           print("+++++++++++++cart")
        else:    
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
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



@login_required(login_url='/user_login/')
def checkout(request, total=0, quantity=0, cart_items=None):
    
    shipping = 40  
    tax = 0
    grand_total = 0
    
    
   
        
    user = request.user
    user_pro, created = User_Profile.objects.get_or_create(user=user)
    user_profile_image_url = user_pro.image.url if user_pro.image else None
    print(user, "user----------------")
    print(user_pro, "user_pro----------------")
        
    user_pro.save()
    print(user_pro,"user_pro----------------")
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        tax = (2 * total)/100
        tax = round(tax,2)
        grand_total = total+tax+shipping
        grand_total = round(grand_total, 2)


    context = {
        'user_pro':user_pro,
        'quantity': quantity,
        'shipping': shipping,
        'cart_items': cart_items,
        'total': total,
        "tax":tax,
        "grand_total":grand_total,
        'user_profile_image_url':user_profile_image_url,
    }
    return render(request, 'checkout.html', context)
