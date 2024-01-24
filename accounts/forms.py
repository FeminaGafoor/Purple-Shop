from django import forms
from .models import User_Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User




class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1','password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = ['phone', 'address', 'city', 'state', 'country', 'image']