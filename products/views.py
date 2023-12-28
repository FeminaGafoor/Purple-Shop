from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from outgoing.models import Cart, CartItem
from outgoing.views import _cart_id
from .models import Category, Product
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


# shop view------------------>

def shop(request, category_slug=None):
 
    categories = None
    product = None

  
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        product = Product.objects.filter(category=categories)
        paginator = Paginator(product, 4)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
    else:
        product = Product.objects.all().order_by('id')
        paginator = Paginator(product, 8)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)


    context = {
        'product': paged_product,
        
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
    
    
def search(request):
    products = []  # Initialize products list
    
    if 'search_product' in request.GET:
        search_product = request.GET['search_product']
        if search_product:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=search_product) | Q(product_name__icontains=search_product))
        
    
    context = {
        'product': products
    }
    return render(request, "shop.html", context)

    