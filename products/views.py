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

        # price_range = request.GET.get('price_range', None)
        # if price_range :
        #     min_price, max_price = get_price_range(price_range)
        #     product = product.filter(price__gte=min_price, price__lte=max_price)


    context = {
        'product': paged_product,
        'category_slug': category_slug,
        
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
    products = []

    if 'search_product' in request.GET:
        search_product = request.GET['search_product']

        if search_product:
            category_slug = request.GET.get('category', '')
            
            # Filter products based on search query
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=search_product) | Q(product_name__icontains=search_product)
            )
            
            # If category_slug is provided, filter products by category
            if category_slug:
                # Filter by category field and then by slug
                products = products.filter(category__slug=category_slug)

    context = {
        'product': products
    }
    return render(request, "shop.html", context)

