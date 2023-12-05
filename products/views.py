from django.shortcuts import get_object_or_404, render

from .models import Category, Product

# Create your views here.



def shop(request, category_slug= None):
    categories = None
    product = None
    
    if category_slug != None:
        
        categories = get_object_or_404(Category, slug= category_slug)
        product = Product.objects.filter(category=categories)
    else:
        product = Product.objects.all()
  
    context = {
        'product': product,
        
    }
    return render(request, "shop.html",context)



def single_product(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        print(single_product,"single_product||||||||||||||||||")
    except Exception as e:
        raise e
    context={
        
        'single_product':single_product,
        
    }
    return render(request, "single_product.html",context)
    