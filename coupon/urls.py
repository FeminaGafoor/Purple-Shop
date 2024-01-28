from django.urls import path
from . import views


app_name='coupon_app'   

urlpatterns = [
    
    path('coupon', views.coupon, name='coupon'),
    
]