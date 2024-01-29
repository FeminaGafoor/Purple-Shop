from django.urls import path
from . import views


app_name='order_app'   

urlpatterns = [
    
    path('place_order/',views.place_order,name='place_order'),
    path('cash_on_delivery/<int:number>', views.cash_on_delivery, name="cash_on_delivery"),
    path('apply_coupon/',views.apply_coupon,name='apply_coupon'),
    path('payments/',views.payments,name='payments'),
    path('order_complete/',views.order_complete,name='order_complete'),
    path('success/',views.success,name='success'),
    
    
    
    # path("payment_status/", views.payment_status, name="payment_status"),
  
    
    
   
]
    