from django.db import models
from django.contrib.auth.models import User
from accounts.models import User_Profile
from products.models import Product, ProductVariant


# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(User_Profile,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_method


class Order(models.Model):
    ORDER_STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Preparing", "Preparing"),
        ("OnShipping", "On Shipping"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
        ("Return", "Return"),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    user_name = models.CharField(max_length=50,)
    # first_name = models.CharField(max_length=50, default=True)
    # last_name = models.CharField(max_length=50, default=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    shipping = models.FloatField(default=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default="New")
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    # tracking_no = models.CharField(max_length = 150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    # def full_name(self):
    #     return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.user_name
    
    
class OrderProduct(models.Model):
    STATUS = (
        ('New' , 'New'),
        ('Accepted' , 'Accepted'),
       ('Cancelled' , 'Cancelled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True) 
    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variant = models.ManyToManyField(ProductVariant, blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices = STATUS, default="New")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_note = models.CharField(blank=True, max_length=100)
     
     
    def __str__(self):
        return self.product.product_name