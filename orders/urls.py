from django.urls import path
from . import views


app_name='order_app'   

urlpatterns = [
    
    path('place_order/',views.place_order,name='place_order'),
    path('cash_on_delivery/<int:number>', views.cash_on_delivery, name="cash_on_delivery"),
    path('success/',views.success,name='success'),
   
  

   
]
    