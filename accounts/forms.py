from django import forms
# from .models import User_Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = User_Profile
#         fields = ['user_name','first_name', 'last_name', 'phone', 'email', 'address_1', 'address_2', 'city', 'state', 'country', 'image']



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email','password1', 'password2', )