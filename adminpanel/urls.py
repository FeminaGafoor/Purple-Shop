from django.urls import path
from . import views

app_name='admin_panel'    

urlpatterns = [
    
    # Admin Authentication Views
    
    
    path('',views.admin_login,name='admin_login'),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    
    
     # User Management
     
    path('user_manage/',views.user_manage,name='user_manage'),
    path('user_block/<int:user_id>/',views.user_block,name='user_block'),
    
   
      # Category Management
      
    path('category_manage/',views.category_manage,name='category_manage'),
    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/',views.edit_category,name='edit_category'),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),
    
    
 
    # Color Management
    
    path('color_manage/',views.color_manage,name='color_manage'),
    path('add_color/',views.add_color,name='add_color'),
    path('edit_color/<int:color_id>',views.edit_color,name='edit_color'),
    path('delete_color/<int:color_id>',views.delete_color,name='delete_color'),
    
     # Size Management
    path('size_manage/',views.size_manage,name='size_manage'),
    path('add_size/',views.add_size,name='add_size'),
    path('edit_size/<int:id>',views.edit_size,name='edit_size'),
    path('delete_size/<int:id>',views.delete_size,name='delete_size'),
    
    
    
    # Product Management
    
    path('product_manage/',views.product_manage,name='product_manage'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/',views.edit_product,name='edit_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    
    # Order Management
    
    path('order_list/',views.order_list,name='order_list'),
]