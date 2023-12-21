import random
import re
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from outgoing.models import Cart, CartItem
from outgoing.views import _cart_id
from .forms import UserProfileForm
from .models import Customer, User_Profile
from django.contrib import auth
from django.core.mail import send_mail



def sign_up(request):
    if request.method == 'POST':
        print("||||||||||||||||||signup")
        #otp with signup----------
        
        get_otp = request.POST.get('otp')
        if get_otp:
            get_email = request.POST.get('email')
            user = Customer.objects.get(email=get_email)
            print(user,"user!!!!!!!!!!!!!!!!!!")
            print("otp")
            
            if not re.search(re.compile(r'^/{6}$'),get_otp):
                messages.error(request,'OTP should only contain numeric!')
                return render(request,'signup.html',{'otp':True,'user':user})
            
            
            session_otp = request.session.get('otp')
            if int(get_otp) == session_otp:
                user.is_active = True
                user.save()
                auth.login(request,user)
                messages.success(request,f'Account is created for {user.username}')
       
                return redirect('account:user_login')
            else:
                messages.warning(request,f'you Entered a Wrong OTP')
 
                return render(request,'signup.html',{'otp':True,'user':user})
 
        else:
            get_otp=request.POST.get('otp1')
            email=request.POST.get('user1')
        if get_otp:
            user=Customer.objects.get(email=email)
            messages.error(request,'field cannot empty!')
            return render(request,'signup.html',{'otp':True,'user':user})
        else:
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')
            repassword=request.POST.get('re_password')
            print("else||||||||||||||||||||")
            # if username.strip() == '' or email.strip() == '' or   password.strip() == '' or repassword.strip() == '': 
            #     messages.info(request , ' field is empty!')
            #     return render(request, 'signup.html')
            if Customer.objects.filter(username=username).exists():
                messages.info(request, ' username is already taken')
                return render(request, 'signup.html')
            elif Customer.objects.filter(email = email).exists():
                    messages.info(request, ' email is already taken')
                    return render(request, 'signup.html')

            elif password != repassword:
                messages.info(request,'Invalid Password')
                return render(request, 'signup.html')
            email_check = validator_email(email)
            if email_check is False:
                messages.info(request, 'email is not valid ')
                return render(request, 'signup.html')
            password_check = validator_password(password)
            if password_check is False:
                messages.info(request, 'Please enter a strong password!')
                return render(request, 'signup.html')
                
        if email_check and password_check:      
            # creating user
            new_user = Customer.objects.create_user(username=username , email= email , password=password )
          
            new_user.save()
            new_user.is_active=False
            new_user.last_login=None
            new_user.save()
            
            
              # Storing the user's email in the session
            request.session['user_email'] = email
            
            user_otp=random.randint(100000,999999)
            request.session['otp']=user_otp
            mess=f'Hello \t{new_user.username},\nOTP to verify your account for Purple Shop  is {user_otp}\n Thanking You!'
            send_mail(
                    "Welcome to Purple Shop, verify your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [new_user.email],

                    fail_silently=False
                )
            return redirect('account:verify_otp')
                
      

    return render(request,'signup.html')
    


def validator_email(email):
    # Basic email format validation using a regular expression
    if re.match(r'^\S+@\S+\.\S+$', email):
        return True
    else:
        return False
    
    

def validator_password(password):
    # Password validation criteria (you can customize these)
    min_length = 6
    if len(password) < min_length:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False
    
    return True



def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        user_email = request.session.get('user_email')  # Retrieve the user's email from the session
        if entered_otp and session_otp and entered_otp == str(session_otp):
            # OTP verification successful
            # Update the user's status to active
            try:
                user = Customer.objects.get(email=user_email)
                user.is_active = True
                user.save()
                auth.login(request, user)
                messages.success(request, f'Enter the OTP send to your mail {user.username}')
                return redirect('account:user_login')
            except Customer.DoesNotExist:
                messages.error(request, 'User not found. Please try registering again.')
        else:
            # OTP verification failed
            messages.warning(request, 'You Entered a Wrong OTP')
            return render(request, 'otp.html', {'otp': True})
    return render(request, 'otp.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.filter(cart=cart)
                
                # product cariants by cart id
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
                # Handle any other exceptions that might occur
                pass
            
            if user:
                # Create or retrieve User_Profile using username
                user_pro, created = User_Profile.objects.get_or_create(user=user, defaults={'user_name': username, 'email': email})
                # Update User_Profile fields
                user_pro.user_name = username
                user_pro.email = email
                # user_pro.phone = phone
                user_pro.save()
                
            login(request, user)
            messages.success(request, "You are now logged in")
             
                # request.session['user'] = email
            return redirect('account:edit_profile')
            
        else:
            messages.error(request, 'Invalid Credentials')

    return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect('home_app:home')



def profile(request):
    
    if request.user.is_authenticated:
        user=request.user
      
        user_pro, created = User_Profile.objects.get_or_create(user=user)
       
        
        user_profile_image_url = user_pro.image.url if user_pro.image else None
        
        # Printing for debugging
        print(user_profile_image_url)

        context = {
            
            'user_pro': user_pro,
            'created': created,
            'user_profile_image_url':user_profile_image_url
        }
        return render(request, 'profile.html',context)
       
        
    return render(request, 'login.html')
    
    
    



def edit_profile(request):
    
    if request.user.is_authenticated:
        try:
            user_profile, created = User_Profile.objects.get_or_create(user=request.user)
        
        except User_Profile.DoesNotExist:
            user_profile = User_Profile(user=request.user)
            
        if request.method == "POST":

            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                user_profile = form.save(commit=False)
                user_profile.user = request.user
            
                user_profile.save()

                # Update the user's email
                user = request.user
                user.email = form.cleaned_data['email']
                user.save()

                messages.success(request, "Profile updated successfully!")
                return redirect('account:profile')
            else:
                messages.error(request, "Please correct the errors in the form.")
        else:
            form = UserProfileForm(instance=user_profile)

        context = {
            'form': form,
        }
        return render(request, 'edit_profile.html', context)