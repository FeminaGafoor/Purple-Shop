from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models import Count, Sum, FloatField
from django.db.models import Sum
from django.db.models.functions import Cast
from django.views import View

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from django.shortcuts import render
from orders.models import Order

from products.models import Category, Product, ProductVariant
from accounts.models import Address, PaymentWallet, User_Profile
from orders.models import Order, OrderProduct, Payment
from coupon.models import Coupon


# Create your views here.




   
# Admin Dashboard---------------------------------

@login_required
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        super_user = User.objects.filter(is_superuser=True).first()
        product_counts = Product.objects.count()
        user_counts = User.objects.count()
        orders_count = Order.objects.filter(status=5).count()

        payment_counts = (
            Payment.objects.values("payment_method")
            .annotate(count=Count("payment_method"))
            .order_by("-count")
        )
        total_payment_count = payment_counts.aggregate(Sum('count'))['count__sum']

        total_transaction_count = Payment.objects.count()

        all_payments = Payment.objects.all()
        total_revenue = sum(Decimal(payment.amount_paid) for payment in all_payments)
        total_sales = Decimal('10000.00')
        revenue_percentage = (total_revenue / total_sales) * 100

        print(f'Total Revenue: {total_revenue}')
        print(f'Revenue Percentage: {revenue_percentage:.2f}%')
        print(revenue_percentage)

        category_wise_order_count = OrderProduct.objects.values('product__category__category_name').annotate(order_count=Count('id'))
        print(category_wise_order_count, "category_wise_order_count||||||||||")

        total_income = Order.objects.aggregate(total_income=Sum('order_total'))['total_income'] or 0
        total_income = round(total_income, 2)
        print(total_income)

        total_sales = Order.objects.aggregate(total_sales=Sum('order_total'))['total_sales'] or 0
        total_sales = round(total_sales, 2)
        print(total_sales)

        # Calculate total income percentage
        income_percentage = (total_income / total_sales) * 100 if total_sales > 0 else 0
        print(income_percentage)

        total_refund_amount = PaymentWallet.objects.aggregate(total_refund=Sum('wallet_balance'))['total_refund']
        total_refund_amount = total_refund_amount or Decimal('0')
        print(total_refund_amount)

        paypal_total_amount = Payment.objects.filter(
            payment_method='PayPal'
        ).annotate(
            amount_paid_float=Cast('amount_paid', FloatField())
        ).aggregate(
            total_amount=Sum('amount_paid_float')
        )['total_amount'] or 0

        print(paypal_total_amount)

        cod_total_amount = Payment.objects.filter(
            payment_method='COD'
        ).annotate(
            amount_paid_float=Cast('amount_paid', FloatField())
        ).aggregate(
            total_amount=Sum('amount_paid_float')
        )['total_amount'] or 0
        cod_total_amount_rounded = round(cod_total_amount, 2)
        print(cod_total_amount_rounded)

        context = {
            "super_user": super_user,
            "product_counts": product_counts,
            "user_counts": user_counts,
            "orders_count": orders_count,
            "total_payment_count": total_payment_count,
            "total_transaction_count": total_transaction_count,
            "revenue_percentage": revenue_percentage,
            "category_wise_order_count": category_wise_order_count,
            "total_income": total_income,
            "income_percentage": income_percentage,
            "total_refund_amount": total_refund_amount,
            "paypal_total_amount": paypal_total_amount,
            "cod_total_amount_rounded": cod_total_amount_rounded,
        }

        return render(request, 'admin_index.html', context)
    else:
        return HttpResponseRedirect('/admin_login/')
    
    
    
    
    
    
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






# Admin logout-------------------------------------


def admin_logout(request):
    
    logout(request)
    return render(request,'admin_login.html')



# User Management---------------------------------


def user_manage(request):
    
    user = User_Profile.objects.all()
    print(user,"user")
    context = {
        'user':user
    }
    return render(request, "user_list.html",context)


def user_block(request,user_id):
    if request.user.is_superuser:
        
        #user is block
        user=User_Profile.objects.get(id = user_id)
        
        if user.is_active:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect('admin_panel:user_manage')
    
    return render(request, "admin_login.html")
        
    
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
            update.product_name = name
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
    

# Product Variant Management-----------------------------------------
def product_variant_manage(request):
    if request.user.is_superuser:
        product_variant = ProductVariant.objects.all()
        
        
        context = {
            'product_variant': product_variant,
           
            
        }

        return render(request, "product_variants.html", context)
    
    return redirect('admin_panel:admin_login')

    

# Add Product Variant -----------------------------------------
    

def add_product_variant(request):
    print("||||||||||||||||||||")
    
    variant_types_choice = (
        ('color', 'Color'),
        ('size', 'Size'),
    )

    if request.user.is_superuser:
        if request.method == "POST":
            product_name = request.POST.get('product_name')
            variant_types = request.POST.get('variant_types') # Ensure that this matches the name attribute in the HTML form
            variant_value = request.POST.get('variant_value')
            quantity = request.POST.get('quantity')
        
            print(variant_types, "|||||||||||||||")

            # Get the Product instance
            product = Product.objects.filter(product_name=product_name).first()

            # Create ProductVariant instance with the selected variant type
            product_variant = ProductVariant.objects.create(
                product=product,
                variant_types=variant_types,
                variant_value=variant_value,
                quantity=quantity,
            )
            product_variant.save()

            messages.success(request, "Product Variant added successfully")
            return redirect('admin_panel:product_manage')

        context = {
            'products': Product.objects.all(),
            'variant_types_choice': variant_types_choice,
        }
        print(context) 
        return render(request, 'product_variant.html', context)

    return redirect('admin_panel:admin_login')


    
# Edit Product Variant -----------------------------------------   


def edit_product_variant(request):
    if request.user.is_superuser:
        if request.method == "POST":
            product_variant_id = request.POST.get('product_variant_id')
            product = request.POST.get('edit_product')
            variant_types = request.POST.get('edit_variant_types')
        
            variant_value = request.POST.get('edit_variant_value')
            quantity = request.POST.get('edit_quantity')
           
            
            product_instance = Product.objects.get(id=product)
            
            update = get_object_or_404(ProductVariant,id=product_variant_id)
            print(update, 'product')
            update.product = product
            update.variant_types = variant_types
            
           
                
            update.variant_value = variant_value
            update.quantity = quantity
       
        
            update.save()
            
            messages.success(request, 'Product updated successfully')
            return redirect('admin_panel:product_manage')
        
        return render(request, 'product_variant_manage.html')
    
    return redirect('admin_panel:admin_login')
    
    
# Delete Product Variant ----------------------------------------- 

    
def delete_product_variant(request,product_variant_id):
    if request.user.is_authenticated:
        product_variant=ProductVariant.objects.get(id=product_variant_id)
        product_variant.delete()
        return redirect('admin_panel:product_variant_manage')
    else:
        return redirect('admin_panel:admin_login')
        
           
    
    
# Coupon Management-----------------------------------------  

 

def coupon_manage(request):
    if request.user.is_superuser:
        coupons = Coupon.objects.all()
        context = {
            'coupons': coupons
            }
        return render(request, 'admin_coupon.html', context)
    
    return redirect('admin_panel:admin_login')


def add_coupon(request):
    if request.method == 'POST':
        coupon_name = request.POST.get('coupon_name')
        coupon_code = request.POST.get('coupon_code')
        coupon_image = request.FILES.get('coupon_image')  # Handle file upload
        coupon_discount = request.POST.get('coupon_discount')
        coupon_minimum_amount = request.POST.get('coupon_minimum_amount')
        coupon_expiration_time = request.POST.get('coupon_expiration_time')

        # Create and save the Coupon object
        coupon = Coupon(
            user=request.user,  # Assuming you have a logged-in user
            offer_name=coupon_name,
            code=coupon_code,
            image=coupon_image,
            discount_price=coupon_discount,
            minimum_amount=coupon_minimum_amount,
            expiration_time=coupon_expiration_time,
        )
        coupon.save()
        
        messages.success(request, 'Coupon added successfully.')
        return redirect('admin_panel:coupon_manage')
    
    return redirect('admin_panel:admin_login')
    
    
    
def edit_coupon(request, id):
    template_name = "edit_coupon.html"
    coupon = get_object_or_404(Coupon, id=id)

    if request.method == 'GET':
        context = {
            "coupon": coupon
        }
        return render(request, template_name, context)
    elif request.method == 'POST':
        # Retrieve form data
        coupon_name = request.POST.get('coupon_name')
        coupon_code = request.POST.get('coupon_code')
        status = request.POST.get('status')
        discount = request.POST.get('coupon_discount')
        minimum_amount = request.POST.get('coupon_minimum_amount')
        coupon_expiration_time = request.POST.get('coupon_expiration_time')
        image = request.FILES.get('image')

        # Update Coupon instance
        coupon.offer_name = coupon_name
        coupon.code = coupon_code
        coupon.is_expired = status == 'true'
        coupon.discount_price = discount
        coupon.minimum_amount = minimum_amount

        # Handle expiration time format conversion
        if coupon_expiration_time:
            coupon.expiration_time = coupon_expiration_time

        if image:
            coupon.image = image

        coupon.save()
        messages.success(request, 'Coupon edited successfully.')
        return redirect('admin_panel:coupon_manage')
    
    
    
def delete_coupon(request, id):
    if request.user.is_superuser:
        coupon = get_object_or_404(Coupon, id=id) 
        coupon.delete()
        messages.success(request, 'Coupon deleted successfully.')
        return redirect('admin_panel:coupon_manage')
    else:
        return redirect('admin_panel:admin_login') 
    
    
    
# <!---------------COUPON ENDS HERE------------>    



def order_list(request):
    url = request.META.get('HTTP_REFERER')

    if request.method == 'GET':
        print("|||||||||||")
        order_status = Order.ORDER_STATUS
        order_products = OrderProduct.objects.all().order_by('created_at')
        unique_order_ids = []
        unique_order_products = []

        for order_product in order_products:
            if order_product.order_id not in unique_order_ids:
                unique_order_ids.append(order_product.order_id)
                unique_order_products.append(order_product)

        context = {
            'order_product': unique_order_products,
            'order_status': order_status,
        }

        return render(request, 'order_list.html', context)

    elif request.method == 'POST':
        selected_status = request.POST.get('orderStatus')
        selected_order_id = request.POST.get('orderId')
        selected_order = get_object_or_404(Order, pk=selected_order_id)
        selected_order.status = selected_status
        selected_order.save()

        return HttpResponseRedirect(url)
                



    

def order_details(request, id):
    print(id,"id|||||||||||||||||||||||||||")

    order_details = Order.objects.get(id=id)
    print(order_details.address,"||||||||||address")
    
    address = Address.objects.filter(user=order_details.user).last()
    print(address,"++++++++")
  
    payment_method = order_details.payment.payment_method if order_details.payment else None

    order_product = OrderProduct.objects.filter(order=order_details)
    
    for product in order_product:
        product_total = product.price*product.quantity
        
    sub_total = sum(product.subtotal() for product in order_product)
 

    tax = (2 * sub_total) / 100
    shipping = 40
    coupon_discount = order_details.coupon.discount_price if order_details.coupon else 0
    grand_total = sub_total + tax + shipping - coupon_discount

    

    context={
        'order_details':order_details,
        'order_status':Order.ORDER_STATUS,
        'sub_total':sub_total,
        'order_product':order_product,
        'tax':tax,
        'product_total':product_total,
        'address':address,
        'shipping': shipping,
        'coupon_discount': coupon_discount,
        'grand_total':grand_total,
        'payment_method':payment_method,
        
    }
    return render(request,'order_details.html',context)






def cancel_product(request, order_id, product_id):
    if order_id and product_id:
        order = get_object_or_404(Order, id=order_id)
        print(order,"order from cancel_product|||||||||||||||||||||||||||||")
        product = get_object_or_404(OrderProduct, id=product_id, order=order)
        print(product,"product from cancel_product|||||||||||||||||||||||||||||||||||")
      
        product.status = 'Cancelled'
        product.save()

       
        return redirect('admin_panel:cancel_list')
    
    

def cancel_list(request):
    canceled_products = OrderProduct.objects.filter(status='Cancelled')
    print(canceled_products,"canceled_products")

    orders = OrderProduct.objects.all().order_by('created_at')
    context={
        'canceled_products': canceled_products,
        'orders':orders,
        'order_status':Order.ORDER_STATUS,

    }

    return render(request,'cancel_list.html',context)




def refund(request,id):
    url = request.META.get('HTTP_REFERER')
    order_product = OrderProduct.objects.get(id=id)
   
    
    print(order_product,"from refund|||||||||||||||||||||||||||||")
    user_wallet = User_Profile.objects.get(user=order_product.order.user)
    print(user_wallet,"user_wallet|||||||||||||||||")
    if order_product.status == 'Cancelled':
        order_product.status = 6
    else:
        order_product.status = 7
        
        
    if order_product.order.coupon:
        print(order_product.order.order_total,"***************************")
        total = order_product.order.order_total - order_product.order.coupon.discount_price
        print(total,"total|||||||||")
        user_wallet.wallet += Decimal(str(total))
    else:
        user_wallet.wallet += Decimal(str(order_product.order.order_total))
    
    
    wallet_details = PaymentWallet(user=order_product.order.user)
    print(wallet_details,"wallet_details||||||||||||||||||||")
    wallet_details.payment_type = "Credit"
    wallet_details.wallet_balance = Decimal(str(order_product.price))
    print(wallet_details.wallet_balance ,"wallet_details.wallet_balance ************************")
    mail_subject = "Your refund has been successfully approved."
    message = render_to_string(
            "refund_recieved_email.html", {"user": order_product.order.user, "wallet": wallet_details.wallet_balance}
        )
    to_email = order_product.order.user.email
    send_mail = EmailMessage(mail_subject, message, to=[to_email])
    send_mail.send()
    
    print("success |||||||||||||||||||||||||||||||||||||||||||||")
    wallet_details.save()
    user_wallet.save()
    order_product.order.save()
    
    return HttpResponseRedirect(url)
        
        
        
        
def sales_report(request):
    order_instance = Order()
    

    context = {
        'order_status_choices': order_instance.ORDER_STATUS
    }

    return render(request, 'sales_report.html', context)      



def generate_report(request):
    
    try:
        order_instance = Order()
        print(order_instance)
        start_date = request.GET.get("start_date")
        print(start_date,"!!!!!!!!!!!!!!")
        end_date = request.GET.get("end_date")
        print(end_date,"!!!!!!!!!!!!!!!")
        status = request.GET.get("status")
        print(status)

        request.session["start_date"] = start_date
        request.session["end_date"] = end_date
        request.session["status"] = status

        filtered_orders = Order.objects.filter(
            created_at__range=[start_date, end_date],
            status=status if status else None,
        ).order_by("created_at")
        print(filtered_orders,"filtered_orders||||||||||")

        context = {
            "sales": filtered_orders,
            'order_status_choices':order_instance.ORDER_STATUS
        }

        return render(request, "sales_report.html", context)
    except Exception as e:
        print(e)
        return render(request, "404.html")
    




def sales_report_pdf(request):
    try:
        start_date = request.session["start_date"]
        end_date = request.session["end_date"]
        status = request.session["status"]

        filtered_orders = Order.objects.filter(
            created_at__range=[start_date, end_date],
            status=status if status else None,
        ).order_by("created_at")

        data = [
            [
                "ID",
                "User",
                "Order Number",
                "Order Date",
                "Status",
                "Tax",
                "Shipping",
                "Grand Total",
            ]
        ]
        
        for sale in filtered_orders:
            data.append(
                [
                    sale.id,
                    sale.user.username,
                    sale.order_number,
                    sale.created_at,
                    sale.get_status_display(),
                    sale.tax,
                    40,
                    sale.order_total,
                ]
            )

        # Create PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="sales_report.pdf"'

        # Create PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        table = Table(data)

        # Apply table styles
        style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )

        table.setStyle(style)
        doc.build([table])

        request.session.pop("start_date", None)
        request.session.pop("end_date", None)
        request.session.pop("status", None)

        return response
    except Exception as e:
        print(e)
        return render(request, "404.html")



