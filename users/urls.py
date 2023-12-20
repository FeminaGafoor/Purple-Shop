from django.urls import path
from . import views


app_name='user_app'   

urlpatterns = [
    path('user_order/',views.user_order,name='user_order'),
    path('order_track/',views.order_track,name='order_track'),
    
   
  

   
]
    