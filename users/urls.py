from django.urls import path
from . import views


app_name='user_app'   

urlpatterns = [
    path('user_order/', views.UserOrderView.as_view(), name='user_order'),
    path('invoice/<int:id>/',views.Invoice.as_view(),name="invoice"),
    path('order_track/<int:id>',views.OrderTrackView.as_view(),name='order_track'),
    
    path("cancel_order/<int:id>/", views.CancelOrder.as_view(), name="cancel_order"),
   
   
  

   
]
    