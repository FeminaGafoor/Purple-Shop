from django.urls import path
from . import views

app_name='account'

urlpatterns = [
    path('',views.user_login,name='user_login'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('otp_func', views.otp_func, name='otp_func'),
    path('new_otp',views.new_otp, name='new_otp'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('address', views.address, name='address'),
    path('add_address', views.add_address, name='add_address'),
    path('edit_address', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    path('change_password', views.change_password, name='change_password'),

]