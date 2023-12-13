from django.contrib import admin
from .models import User_Profile



# Register your models here.
    
class User_ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'phone','email','image')

admin.site.register(User_Profile,User_ProfileAdmin)