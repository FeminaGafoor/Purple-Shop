

from django.contrib.auth.models import User
from django.db import models
from coupon.models import Coupon



# Create your models here.

    
class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField(null=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True,blank=True)

    image = models.ImageField( upload_to='images/',blank=True,null=True)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        print(f"User instance: {self.user}")
        return self.user.username


    @property
    def user_name(self):
        print(f"User first_name: {self.user.first_name}")
        print(f"User last_name: {self.user.last_name}")
        return f"{self.user.first_name} {self.user.last_name}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=20)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15,default=True,null=True)
    country = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.username