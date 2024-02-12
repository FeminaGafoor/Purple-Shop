from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductVariant

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug', 'display_image')

   
    def display_image(self, obj):
        if obj.category_image:
            return format_html('<img src="{}" width="110" height="70" />', obj.category_image.url)
        else:
            return "No Image"

    display_image.short_description = 'Category Image'
    

    
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'price', 'stock', 'category', 'created_date', 'is_available' ,'display_image')
    
    def display_image(self, obj):
        if obj.images:
            return format_html('<img src="{}" width="80" height="70" />', obj.images.url)
        else:
            return "No Image"

    display_image.short_description = 'Product Image'
    
      
    
    
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'variant_types','variant_value','quantity','created_at','is_active')
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product,ProductAdmin)
# admin.site.register(Color,ColorAdmin)
# admin.site.register(Size)
admin.site.register(ProductVariant, ProductVariantAdmin)



