from django.http import Http404, HttpResponse, JsonResponse
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
    

# search--------------------------->


def search(request):
    products = []
    print("!!!!!!!!!!!!!!!!!!!!!11")
    if 'search_product' in request.GET:
        search_product = request.GET['search_product']
        print(search_product,"search_product")
        if search_product:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=search_product) | Q(product_name__icontains=search_product)
            )
           
    context = {
        'product': products
    }
    return render(request, "shop.html", context)




from django.http import JsonResponse

def get_product_suggestions(request):
    search_query = request.GET.get('search_query', '')
    suggestions = []

    if search_query:
        products = Product.objects.filter(title__icontains=search_query)
        suggestions = [product.title for product in products]

    return JsonResponse({'suggestions': suggestions})




# search ends --------------------------->


# filter--------------------------->

def filter(request):

    price_range = request.GET.get('price_range', 'All')
    if price_range == 'All':
        products = Product.objects.filter(is_available=True).order_by('id')
    else:
        min_price, max_price = price_range.split('-')
        products = Product.objects.filter(price__range=(min_price, max_price), is_available=True).order_by('id')
        

    serialized_products = [
        {
            'product_name': product.product_name,
            'price': product.price,
            'images': product.images,
        } for product in products
    ]
    print(serialized_products,"serialized_products!!!!!!!!!!!!!")

    context = {'product': serialized_products}

    return render(request, 'shop.html', context)


# filter ends--------------------------->

def contact(request):
    
    return render(request, "contact.html")
    

