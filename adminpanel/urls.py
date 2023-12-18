from django.urls import path
from . import views

app_name='admin_panel'    

urlpatterns = [
    
    # Admin Authentication Views
    
    
    path('',views.admin_login,name='admin_login'),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    
    
     # User Management
     
    path('user_list/',views.user_list,name='user_list'),
    
   
      # Category Management
      
    path('category_manage/',views.category_manage,name='category_manage'),
    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/',views.edit_category,name='edit_category'),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),
 
 
  
    
    # Product Management
    
    path('product_manage/',views.product_manage,name='product_manage'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/',views.edit_product,name='edit_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    
    # Order Management
    
    path('order_list/',views.order_list,name='order_list'),
]