from django.urls import path
from . import views


app_name='order_app'   

urlpatterns = [
    # path('order_place/',views.order_place,name='order_place'),
    path('payment/',views.payment,name='payment'),
    path('success/',views.success,name='success'),
   
  

   
]
    