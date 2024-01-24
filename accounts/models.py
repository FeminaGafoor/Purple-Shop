from django.contrib.auth.models import User
from django.db import models


# Create your models here.

    
class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField(null=True)
    address = models.CharField(max_length=20)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15,default=True,null=True)
    country = models.CharField(max_length=15)
    image = models.ImageField( upload_to='images/',blank=True,null=True)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.user.username

    def user_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
