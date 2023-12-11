from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Customer(User):
    
    otp = models.IntegerField(blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.username
    
class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.BigIntegerField(null=True)
    email = models.EmailField(max_length=30)
    address_line_1 = models.CharField(max_length=20)
    address_line_2 = models.CharField(max_length=20,blank=True,null=True)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15,default=True,null=True)
    country = models.CharField(max_length=15)
    image = models.ImageField( upload_to='images/',blank=True,null=True)

    def __str__(self) :
        return self.user_name