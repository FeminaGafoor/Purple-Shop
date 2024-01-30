from django.urls import path
from . import views


# Create your views here.

app_name='coupon_app'   

urlpatterns = [
    path('coupon', views.coupon, name='coupon'),
]