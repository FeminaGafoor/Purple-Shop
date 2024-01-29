import random
import re
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from outgoing.models import Cart, CartItem
from outgoing.views import _cart_id
from django.contrib.auth.models import User

from coupon.models import Coupon
from .models import  User_Profile
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from accounts.forms import SignUpForm


# -------------------------SIGN_UP-------------------------


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            print(username)
            password = form.cleaned_data.get('password1')
            print(password)
            email = form.cleaned_data.get('email')
            print(email)
            
            otp = str(random.randint(1000, 9999))
            print(otp)
            request.session['signup_username']=username
            request.session['signup_otp'] = otp
  
            subject = 'OTP Verification Code'
            message = f'Your OTP code for signup is: {otp}'
            from_email = 'femitest.111@gmail.com'
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list)
            
            messages.success(request, 'Your account has been created!Please Enter OTP')
            return redirect('account:otp_func')
        else:
            messages.warning(request,form.errors)
            return redirect('account:sign_up')

    return render(request, 'signup.html')

    
# -------------------------SIGN_UP ENDED-------------------------


# -------------------------GENERATE OTP----------------------------------

def otp_func(request):
    
    if request.method == 'POST':
        otp_entered = request.POST.get('otp_entered')
        otp_saved = request.session.get('signup_otp')
        
        if otp_entered == otp_saved:
            # OTP is valid; remove it from the session
            del request.session['signup_otp']

            # Save the user
            username=request.session['signup_username']
            user = User.objects.get(username=username)
            user.is_active = True
            user.is_otp=True
            user.save()
            messages.success(request, "Your registration is successful. You can now log in.")           
            return redirect('account:user_login')  
        
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request,'otp.html')



def new_otp(request):
    
    username=request.session.get('signup_username')
    user = User.objects.get(username=username)
    request.session.pop('signup_otp', None)
  
    if user.email:
        otp = str(random.randint(1000, 9999))
        request.session['signup_otp'] = otp
        subject = 'Resent OTP Verification Code'
        message = f'Your resent OTP code for signup is: {otp}'
        from_email = 'femitest.111@gmail.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'resend OTP sent successfully. Please check your email.')
    else:
        messages.warning(request, 'Failed to resend OTP. Please try again.')

    return redirect('account:otp_func')


# -------------------------GENERATE OTP ENDED-------------------------



# -------------------------USER LOGIN ---------------------------------

def user_login(request):
    print("+++++++++++++++++++++")
    if request.method == "POST":
        email = request.POST.get('email')
        print(email,"email")
        password = request.POST.get('password')
        print(password,"password")
        user = authenticate(request, email=email, password=password)

        print(user,"from login")
        if user is not None:
            print("not none")
            if user.email != email:
                messages.error(request, 'Invalid Credentials')
                return render(request, 'login.html')
            
            try:
                
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    # product variants by cart id
                    product_variants = []
                    for item in cart_item:
                        variants = item.product_variant.all()
                        product_variants.append(list(variants))
                
                    #  get cart_items from user to access product_variation   
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list=[]
                    id = []
                    for item in cart_item:
                        existing_variation = item.product_variant.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                
                    for pro in product_variants:
                        if pro in ex_var_list:
                            index = ex_var_list.index(pro)
                            item_id = id[index]
                            item = CartItem.objects.get(id = item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        
                        else:
                            cart_item = CartItem.objects.filter(cart = cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
                
                
            except Exception as e:
                print("Exception occurred:", e)
                pass
            
            if user:
                user_pro, created = User_Profile.objects.get_or_create(user=user)
                user_pro.email = email
                # user_pro.user_name
                print(user_pro.email,"___________________________")
                coupon = Coupon.objects.first()  # Get the first coupon, you may adjust this based on your logic
                user_pro.coupon = coupon
                user_pro.save()
                
            login(request, user)
            messages.success(request, "You are already a user,log in now")
             
            return redirect('account:edit_profile')
            
        else:
            messages.error(request, 'Invalid Credentials')

    return render(request, 'login.html')

# -------------------------USER LOGIN ENDED-------------------------


# -------------------------USER LOGOUT -------------------------


@login_required(login_url='/user_login/')
def user_logout(request):
    logout(request)
    return redirect('home_app:home')


# -------------------------USER LOGOUT ENDED-------------------------



# -------------------------CREATE USER PROFILE-------------------------


@login_required(login_url='/user_login/') 
def profile(request):
    
    if request.user.is_authenticated:
        user=request.user
        user_pro, created = User_Profile.objects.get_or_create(user=user)
        user_profile_image_url = user_pro.image.url if user_pro.image else None
        
        
        print(user_pro)
        print(user_pro.user_name,"|||||||||||||||||||||||||||||||||||||||||")
        print(user_pro.user.first_name)
        print(user_pro.user.last_name)
        # Printing for debugging
        print(user_profile_image_url)

        context = {
            
            'user_pro': user_pro,
            # 'created': created,
            'user_profile_image_url':user_profile_image_url
        }
        return render(request, 'profile.html',context)
       
        
    return render(request, 'login.html')
    
    
    
# -------------------------EDIT USER PROFILE-------------------------

    
    
@login_required(login_url='/user_login/')  
def edit_profile(request):
    print("|||||||||||||||||from edit")
    if request.method == "POST":
        username = request.POST["user_name"]
        email = request.POST["email"]
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        phone = request.POST["phone"]
        country = request.POST["country"]
        state = request.POST["state"]
        city = request.POST["city"]
        address = request.POST["address"]
        image = request.FILES.get("image")
        
        print("|||||||||||||||||from")

        # Get or create the User instance based on the username
        user_form, created = User.objects.get_or_create(username=username)
        user_form.email = email
        user_form.first_name = firstname
        user_form.last_name = lastname
        user_form.save()
        print("|||||||||||||||||from|||||||||||||||||||||||")
        # Get or create the UserProfile instance associated with the User
        profile, created = User_Profile.objects.get_or_create(user=user_form)
        profile.phone = phone
        profile.country = country
        profile.city = city
        profile.state = state
        profile.address = address
        if image:
            profile.image = image
        coupon = Coupon.objects.first()  # Get the first coupon, you may adjust this based on your logic
        profile.coupon = coupon
        profile.save()
        
        print(profile.phone,"+++++++++++++++++++((((((((((((((((((((()))))))))))))))))))))")
        return redirect('account:profile')
    else:
        
        user_form = request.user  # Assuming the request.user is authenticated
        profile, created = User_Profile.objects.get_or_create(user=user_form)

    context = {
        "user_form": user_form,
        "profile": profile,
    }

    return render(request, "edit_profile.html", context)    
    
    
    
    
# -------------------------USER PROFILE ENDED-------------------------  


 
# -------------------------USER'S COUPON-------------------------  

    
    
    
    
   
# -------------------------USER'S COUPON ENDED-------------------------  


  
@login_required(login_url='/accounts/user_login/')    
def change_password(request):
    
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user_profile = request.user.user_profile  # Access the User_Profile instance
        user = user_profile.user  # Access the associated User instance
        
        if new_password == confirm_password:
            # Use check_password on the User instance
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
             
                messages.success(request,"Password updated successfully")
                return redirect('account:change_password')
            else:
                messages.error(request,"Please enter valid current password")
                return redirect('account:change_password')
        else:
            messages.error(request,"Password does not match")
            return redirect('account:change_password')
    
    return render(request, 'change_password.html')
    
