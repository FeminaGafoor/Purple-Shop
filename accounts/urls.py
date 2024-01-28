from django.urls import path
from . import views

app_name='account'

urlpatterns = [
    path('',views.user_login,name='user_login'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('otp_func', views.otp_func, name='otp_func'),
    path('new_otp',views.new_otp, name='new_otp'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    # path('coupon', views.coupon, name='coupon'),
    path('change_password', views.change_password, name='change_password'),

]