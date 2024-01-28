from django.db import models
from django.contrib.auth.models import User
from products.models import Product, ProductVariant
from coupon.models import Coupon

# Create your models here.
    
 
 
 # cart model---------
    
    
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True )
    coupons = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variant = models.ManyToManyField(ProductVariant, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product.product_name
    
    

    @property
    def price(self):
        if self.product:  # Check if product exists
            return self.product.price
        return 0  # or any default value you prefer

    @property
    def amount(self):
        if self.product and self.product.price:  # Check if product and its price exist
            return self.quantity * self.product.price

        if self.coupons:
            return self.product.price - self.coupons.discount_price