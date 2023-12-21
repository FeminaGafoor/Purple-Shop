from django.urls import path
from . import views


app_name='user_app'   

urlpatterns = [
    path('user_order/', views.UserOrderView.as_view(), name='user_order'),
    path('order_track/<int:id>',views.OrderTrackView.as_view(),name='order_track'),
    
   
  

   
]
    