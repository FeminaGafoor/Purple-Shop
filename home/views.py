from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from products.models import Category, Product

# Create your views here.

def home(request):
    
    product = Product.objects.all()[:8]
    categories = Category.objects.all()
    

    context = {
        'product': product,
        'categories' : categories,
      
    }
    return render(request, "index.html",context)


