
from django.db.models import Q 
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login,logout
from products.models import Category, Product
from django.utils.text import slugify

# Create your views here.


# Admin authentiction----------------------------------

def admin_login(request):
    
    if request.method == "POST":
        username = request.POST['user_name']
        password = request.POST['password']
        
        user_obj = authenticate(request, username=username, password=password)
        
        if user_obj is not None:
            if user_obj.is_superuser:
                login(request, user_obj)
                return redirect('admin_panel:admin_dashboard')
            else:
                messages.error(request, "User is not authenticated")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "admin_login.html")



# Admin Dashboard---------------------------------


def admin_dashboard(request):
      
    if not request.user.is_superuser:
        return render(request,'admin_login.html')
    
    return render(request, "admin_index.html")


# Admin logout-------------------------------------


def admin_logout(request):
    
    logout(request)
    return render(request,'admin_login.html')



# User Management---------------------------------


def user_list(request):
    return render(request, "user_list.html")


    
    
# Category Management------------------------------


def category_manage(request):
    
    category = Category.objects.all()
    context={
        'category':category
    }
   
    return render(request, "category_list.html",context)



# Add category---------------------------------------


def add_category(request):
    if request.user.is_superuser:
        if request.method == "POST":
            category_name = request.POST.get('name')
            category_image = request.FILES.get('image')
            category_description = request.POST.get('description')
            print(category_image,"|||||||||||||||||")
            
            if category_name.strip() == '':
                messages.error(request, 'field is empty!')
                return redirect('admin_panel:add_category')
        
            existing_category = Category.objects.filter(
                Q(category_name__iexact=category_name)
            ).first()

            if existing_category:
                messages.error(request, 'The entered category is already taken')
                return redirect('admin_panel:add_category')
            
            elif not category_image:
                messages.error(request, 'image is not uploaded!')
                return redirect('admin_panel:add_category')
            
            elif category_description.strip() == '':
                messages.error(request, 'description is not given!')
                return redirect('admin_panel:add_category')
            
            else:
                slug = slugify(category_name)
                new_category =  Category.objects.create(
                    category_name=category_name, 
                    category_description=category_description, 
                    category_image=category_image, 
                    slug=slug
                    )
                
                new_category.save()
                messages.success(request,"Categories are added successfully")
                return redirect('admin_panel:category_manage')
        else:
            return redirect('admin_panel:category_manage')   
        
    return render(request, "admin_login.html")




# Edit category-----------------------------------------
    
    
    
def edit_category(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            category_id = request.POST.get('category_id')
            category_name = request.POST.get('edit_name')
            category_image = request.FILES.get('edit_image')
            description = request.POST.get('edit_description')
            
            
             #---validate the form data-----

            if category_name.strip() == "":
                messages.error(request,"Field is empty!")
                return redirect('admin_panel:category_manage')
            
            existing_category = Category.objects.filter(
                Q(category_name__iexact=category_name)
            ).first()

            if existing_category:
                messages.error(request, 'The entered category is already taken')
                return redirect('admin_panel:add_category')
            
            elif not category_image:
                messages.error(request, 'Image is not uploaded!')
                return redirect('admin_panel:category_manage')
            elif description.strip() == '':
                messages.error(request, 'Description is not given!')
                return redirect('admin_panel:category_manage')
    
            # Update the category instance
        
            update = get_object_or_404(Category,id=category_id)
            update.category_name = category_name
            update.category_image = category_image
            update.category_description = description
        
            update.save()
            messages.success(request, 'Category updated successfully')
            return redirect('admin_panel:category_manage')
        else:
            return redirect('admin_panel:category_manage') 
    else:
        return redirect('admin_panel:admin_login')


#Delete Category--------------------------------------



def delete_category(request,category_id):
    
    if request.user.is_superuser:
        
        category = get_object_or_404(Category, id=category_id)
        
        category.delete()
        return redirect('admin_panel:category_manage')
    else:
        return redirect('admin_panel:admin_login')
    



# Product Management------------------------------------

def product_manage(request):
    if request.user.is_superuser:
        product = Product.objects.all()
        category = Category.objects.all()
        
        context = {
            'product': product,
            'category' : category
            
        }

        return render(request, "product_list.html", context)
    
    return redirect('admin_panel:admin_login')



# Add Product-----------------------------------------


def add_product(request):
    if request.user.is_superuser:
        
        
        if request.method == "POST":
            name = request.POST.get('name')
            description = request.POST.get('description')
            images = request.FILES.get('images')
            price = request.POST.get('price')
            category_name = request.POST.get('category')
            stock = request.POST.get('stock')
      
            if not images:
                messages.error(request, 'Image is not uploaded!')
                return redirect('admin_panel:product_manage')
     
            try:
                product_instance = Product.objects.get(product_name=name)
                messages.error(request, 'Product with this name already exists.')
                return redirect('admin_panel:product_manage')
            except Product.DoesNotExist:
                pass
      
            category_instance, created = Category.objects.get_or_create(category_name=category_name)
            
            slug = slugify(name)
            product = Product.objects.create(
                product_name = name,
                description =description,
                images = images,
                category = category_instance,
                price = price,
                stock = stock,
                slug = slug,
            )
            product.save()
            messages.success(request,"Products are added successfully")
           
            
            return redirect('admin_panel:product_manage')
    
    return redirect('admin_panel:admin_login')


# Edit Product-----------------------------------------



def edit_product(request):
    
    if request.user.is_superuser:
        if request.method == "POST":
            product_id = request.POST.get('product_id')
            name = request.POST.get('edit_name')
            description = request.POST.get('edit_description')
            images = request.FILES.get('edit_image')
            price = request.POST.get('edit_price')
            category_name = request.POST.get('category')
            stock = request.POST.get('edit_stock')
            
            category_instance = Category.objects.get(id=category_name)
            
            update = get_object_or_404(Product,id=product_id)
            print(update, 'product')
            update.name = name
            update.description = description
            
            if images:
                update.images = images
                
            update.price = price
            update.category = category_instance
            update.stock = stock
        
            update.save()
            
            messages.success(request, 'Product updated successfully')
            return redirect('admin_panel:product_manage')
        
        return render(request, 'product_manage.html')
        
    else:

        return redirect('admin_panel:admin_login')
    

# Delete Product-----------------------------------------
    
def delete_product(request, product_id):
    if request.user.is_superuser:
        product = get_object_or_404(Product, id=product_id) 
        product.delete()
        return redirect('admin_panel:product_manage')
    else:
        return redirect('admin_panel:admin_login')
    
    
    
def order_list(request):
    return render(request,'order_list.html')
    