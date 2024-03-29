from django.urls import reverse
from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.

# category model---------


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_description = models.CharField(max_length=50, unique=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to='photos/categories', blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def get_url(self):
        return reverse('shop_app:products_by_category', args=[self.slug])
    
    def __str__(self):
        return self.category_name


  
    
# product model---------

    
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='photos/products',)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    
    
    def get_url(self):
        return reverse('shop_app:single_product', args=[self.category.slug ,self.slug])
    
    def __str__(self):
        return self.product_name
    
    
class VariantManager(models.Manager):
    def colors(self):
        return super(VariantManager, self).filter(variant_types='color', is_active= True) 
    
    def sizes(self):
        return super(VariantManager, self).filter(variant_types='size', is_active= True)  
    
variant_types_choice = (
    ('color','color'),
    ('size','size'),
)   
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant_types = models.CharField(max_length=100,choices = variant_types_choice)
    variant_value = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    
    objects = VariantManager()
    
    def __str__(self):
        return self.variant_value
