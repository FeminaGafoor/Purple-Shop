from django.urls import path
from . import views


app_name='order_app'   

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payment/',views.payment,name='payment'),
    
  

   
]
    