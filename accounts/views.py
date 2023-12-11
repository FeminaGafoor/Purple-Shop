# import random
# import re
# from django.conf import settings
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login
# from django.contrib import messages
# from outgoing.models import Cart, CartItem
# from outgoing.views import _cart_id
# from .models import Customer
# from django.contrib import auth
# from django.core.mail import send_mail



# def sign_up(request):
#     if request.method == 'POST':
#         print("!!!!!!!!!!!!!!!!!!")
        
#         #otp with signup----------
        
#         get_otp = request.POST.get('otp')
#         if get_otp:
#             get_email = request.POST.get('email')
#             user = Customer.objects.get(email=get_email)
#             print(user,"user!!!!!!!!!!!!!!!!!!")

            
#             if not re.search(re.compile(r'^/{6}$'),get_otp):
#                 messages.error(request,'OTP should only contain numeric!')
#                 return render(request,'signup.html',{'otp':True,'user':user})
            
            
#             session_otp = request.session.get('otp')
#             if int(get_otp) == session_otp:
#                 user.is_active = True
#                 user.save()
#                 auth.login(request,user)
#                 messages.success(request,f'Account is created for {user.username}')
       
#                 return redirect('account:user_login')
#             else:
#                 messages.warning(request,f'you Entered a Wrong OTP')
 
#                 return render(request,'signup.html',{'otp':True,'user':user})
 
#         else:
#             get_otp=request.POST.get('otp1')
#             email=request.POST.get('user1')
#         if get_otp:
#             user=Customer.objects.get(email=email)
#             messages.error(request,'field cannot empty!')
#             return render(request,'signup.html',{'otp':True,'user':user})
#         else:
#             username=request.POST.get('username')
#             email=request.POST.get('email')
#             password=request.POST.get('password')
#             repassword=request.POST.get('re_password')
          
#             # if username.strip() == '' or email.strip() == '' or   password.strip() == '' or repassword.strip() == '': 
#             #     messages.info(request , ' field is empty!')
#             #     return render(request, 'signup.html')
#             if Customer.objects.filter(username=username).exists():
#                 messages.info(request, ' username is already taken')
#                 return render(request, 'signup.html')
#             elif Customer.objects.filter(email = email).exists():
#                     messages.info(request, ' email is already taken')
#                     return render(request, 'signup.html')

#             elif password != repassword:
#                 messages.info(request,'Invalid Password')
#                 return render(request, 'signup.html')
#             email_check = validator_email(email)
#             if email_check is False:
#                 messages.info(request, 'email is not valid ')
#                 return render(request, 'signup.html')
#             password_check = validator_password(password)
#             if password_check is False:
#                 messages.info(request, 'Please enter a strong password!')
#                 return render(request, 'signup.html')
                
#         if email_check and password_check:      
#             # creating user
#             new_user = Customer.objects.create_user(username=username , email= email , password=password )
          
#             new_user.save()
#             new_user.is_active=False
#             new_user.last_login=None
#             new_user.save()
            
            
#               # Storing the user's email in the session
#             request.session['user_email'] = email
            
#             user_otp=random.randint(100000,999999)
#             request.session['otp']=user_otp
#             mess=f'Hello \t{new_user.username},\nOTP to verify your account for Luxury Shop  is {user_otp}\n Thanking You!'
#             send_mail(
#                     "Welcome to Luxury Shop, verify your Email",
#                     mess,
#                     settings.EMAIL_HOST_USER,
#                     [new_user.email],

#                     fail_silently=False
#                 )
#             return redirect('account:verify_otp')
                
      

#     return render(request,'signup.html')
    


# def validator_email(email):
#     # Basic email format validation using a regular expression
#     if re.match(r'^\S+@\S+\.\S+$', email):
#         return True
#     else:
#         return False
    
    

# def validator_password(password):
#     # Password validation criteria (you can customize these)
#     min_length = 6
#     if len(password) < min_length:
#         return False

#     if not any(char.isupper() for char in password):
#         return False

#     if not any(char.islower() for char in password):
#         return False

#     if not any(char.isdigit() for char in password):
#         return False
    
#     return True



# def verify_otp(request):
#     if request.method == 'POST':
#         entered_otp = request.POST.get('otp')
#         session_otp = request.session.get('otp')
#         user_email = request.session.get('user_email')  # Retrieve the user's email from the session

#         if entered_otp and session_otp and entered_otp == str(session_otp):
#             # OTP verification successful
#             # Update the user's status to active
#             try:
#                 user = Customer.objects.get(email=user_email)
#                 user.is_active = True
#                 user.save()
#                 auth.login(request, user)
#                 messages.success(request, f'Account is created for {user.username}')
#                 return redirect('account:user_login')
#             except Customer.DoesNotExist:
#                 messages.error(request, 'User not found. Please try registering again.')
#         else:
#             # OTP verification failed
#             messages.warning(request, 'You Entered a Wrong OTP')
#             return render(request, 'otp.html', {'otp': True})
#     return render(request, 'otp.html')




# def user_login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Use authenticate for user authentication
#         user = authenticate(request, username=username, password=password)

#         # if user is not None:
#         #     try:
#         #         # Handle cart-related logic
#         #         cart = get_object_or_404(Cart, cart_id=_cart_id(request))
#         #         check_variant = CartItem.objects.filter(cart=cart)

#         #         if check_variant:
#         #             cart_pro = CartItem.objects.filter(cart=cart)
#         #             for product in cart_pro:
#         #                 product.user = user
#         #                 product.save()
#         #     except Exception as e:
#         #         # Log or handle exceptions appropriately
#         #         print(f"Error handling cart: {e}")

#             # Log in the user using Django's login function
#         login(request, user)
#         request.session['user'] = email
#         return redirect('home_app:home')
#     else:
#         messages.error(request, 'Invalid Credentials')

#     return render(request, 'login.html')

