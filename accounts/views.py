from base64 import urlsafe_b64decode
from email.message import EmailMessage
import random
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from outgoing.models import Cart, CartItem
from outgoing.views import _cart_id
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from coupon.models import Coupon
from .models import  Address, User_Profile
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from accounts.forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage



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
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            
            
            send_mail(subject, message, from_email, recipient_list)
            
            messages.success(request, 'Your account has been created! Please enter OTP send to your mail')
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
        from_email = 'purpleshop.tech@gmail.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'resend OTP sent successfully. Please check your email.')
    else:
        messages.warning(request, 'Failed to resend OTP. Please try again.')

    return redirect('account:otp_func')


# -------------------------GENERATE OTP ENDED-------------------------



# -------------------------USER LOGIN ---------------------------------

def user_login(request):
    
    if request.method == "POST":
        email = request.POST.get('email')
        print(email,"email")
        password = request.POST.get('password')
        print(password,"password")
        user = authenticate(request, email=email, password=password)

        
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
                    
                    #----------- product variants by cart id---------
                    product_variants = []
                    for item in cart_item:
                        variants = item.product_variant.all()
                        product_variants.append(list(variants))
                
                    #  ---------get cart_items from user to access product_variation  --------- 
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
                user_pro.user_name
                print(user_pro.email,"___________________________")
                coupon = Coupon.objects.first()
                user_pro.coupon = coupon
                user_pro.save()
                
            login(request, user)
            messages.success(request, "You are already a user,Create your profile")
             
            return redirect('account:edit_profile')
            
        else:
            messages.error(request, 'Invalid Credentials')

    return render(request, 'login.html')


# -------------------------USER LOGIN ENDED-------------------------


# -------------------------USER LOGOUT -------------------------


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='/user_login/')
def user_logout(request):
    logout(request)
    return redirect('home_app:home')



# -------------------------USER LOGOUT ENDED-------------------------



# -------------------------FORGOT PASSWORD-------------------------




def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
 

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
     

            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string(
                "reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            to_email = email
            send_mail = EmailMessage(
                mail_subject,
                message,
                to=[to_email],  # 'to' argument should be passed here, not in MIMEPart
            )
            send_mail.send()

            messages.success(
                request, "Password reset email has been sent to your email address"
            )
         
            return redirect('account:user_login')
        else:
            messages.error(request, "Account does not exist")
            return redirect("account:forgot_password")

    return render(request, "forgot_password.html")





def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_b64decode(uidb64).decode()
        print(uid,"from reset password validator")
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
  
        request.session["uid"] = uid
        messages.success(request, "please reset your password")
       
        return redirect("account:reset_password")
    else:
       
        messages.success(request, "this link has been expired!")
        return redirect("account:user_login")
    
    
    
    
    
def reset_password(request):

    if request.method == "POST":
  
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            uid = request.session.get("uid")
            
            if uid is not None:
                user = User.objects.get(pk=uid)
                user.set_password(password)
                user.save() 
                print("user saved")
            messages.success(request, "Password Reset Successful")
            return redirect("account:user_login")
        else:
            messages.error(request, "password do not match")
            return redirect("account:reset_password")
    return render(request, "reset_password.html")





# -------------------------FORGOT PASSWORD ENDED-------------------------



# -------------------------CREATE USER PROFILE-------------------------



@login_required(login_url='/user_login/') 
def profile(request):
    
    if request.user.is_authenticated:
        user=request.user
        user_pro, created = User_Profile.objects.get_or_create(user=user)
        user_profile_image_url = user_pro.image.url if user_pro.image else None
        
        
        context = {
            
            'user_pro': user_pro,
            'created': created,
            'user_profile_image_url':user_profile_image_url
        }
        return render(request, 'profile.html',context)
       
        
    return render(request, 'login.html')
    
    
    
# -------------------------EDIT USER PROFILE-------------------------

    
    
@login_required(login_url='/user_login/')  
def edit_profile(request):
    
    if request.method == "POST":
        username = request.POST["user_name"]
        email = request.POST["email"]
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        phone = request.POST["phone"]
        image = request.FILES.get("image")
        
        user_form, created = User.objects.get_or_create(username=username)
        user_form.email = email
        user_form.first_name = firstname
        user_form.last_name = lastname
        user_form.save()
        
        # Get or create the UserProfile instance associated with the User
        profile, created = User_Profile.objects.get_or_create(user=user_form)
        profile.phone = phone
        
        
        if image:
            profile.image = image
        
        coupon = Coupon.objects.first()  
        profile.coupon = coupon
        profile.save()
        
        
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


 
# ------------------------- ADDRESS-------------------------  

def address(request):
    
  
    user_pro, created = User_Profile.objects.get_or_create(user=request.user)
    
    user_address = Address.objects.filter(user=request.user)
   
    context = {
        "user_pro":user_pro,
        "user_address": user_address,
        
    }
    return render(request, "checkout.html", context)


# -------------------------ADD ADDRESS------------------------- 


def add_address(request):
    if request.method == "POST":
   
        count = Address.objects.filter(user=request.user).count()

        if count >=  2:
  
     
            messages.error(request, "Maximum of two addresses are allowed.")
            return redirect("outgoing_app:checkout")

      
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        

        user_address = Address.objects.create(
            user=request.user,
            new_name=user_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            country=country,
            
        )
        user_address.save()

        messages.success(request, "Successfully added")
        return redirect("outgoing_app:checkout")


    return redirect("outgoing_app:checkout")
        
        
# -------------------------EDIT ADDRESS------------------------- 
    
def edit_address(request):
   
    user_address_id = request.POST.get("user_id")
    user_address = get_object_or_404(Address, id=user_address_id)

    if request.method == "POST":
        # Update the fields based on the form data
        user_address.new_name = request.POST["edit_new_name"]
        user_address.email = request.POST["edit_email"]
        user_address.phone = request.POST["edit_phone"]
        user_address.address = request.POST["edit_address"]
        user_address.city = request.POST["edit_city"]
        user_address.state = request.POST["edit_state"]
        user_address.country = request.POST["edit_country"]

        # Save the updated address
        user_address.save()

        messages.success(request, 'Address updated successfully')
        return redirect('account:address')

    
    return render(request, "checkout.html")    
    
   
# -------------------------DELETE ADDRESS -------------------------  

def delete_address(request,id):
    
    user_address = get_object_or_404(Address, id=id)
    user_address.delete()

    return redirect('account:address')
   



# -------------------------CHANGE PASSWORD------------------------- 
  
@login_required(login_url='/account/user_login/')    
def change_password(request):
 
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user_profile = request.user.user_profile  # Access the User_Profile instance
        user = user_profile.user  # Access the associated User instance
       
        if new_password == confirm_password:
            
            success = user.check_password(current_password)
           
            if success:
                user.set_password(new_password)
                user.save()
                
                logout(request)
                
                messages.success(request,"Password updated successfully")
                return redirect('home_app:home')
            else:
                messages.error(request,"Please enter valid current password")
                return redirect('account:change_password')
        else:
            messages.error(request,"Password does not match")
            return redirect('account:change_password')
    
    return render(request, 'change_password.html')
    
    
    
# -------------------------CHANGE PASSWORD ENDED------------------------- 
