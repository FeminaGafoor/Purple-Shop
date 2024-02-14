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
    
    
    # Product Management
    
    path('product_manage/',views.product_manage,name='product_manage'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/',views.edit_product,name='edit_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    
      # Product Variant Management
    
    path('product_variant_manage/',views.product_variant_manage,name='product_variant_manage'),
    path('add_product_variant/',views.add_product_variant,name='add_product_variant'),
    path('edit_product_variant/',views.edit_product_variant,name='edit_product_variant'),
    path('delete_product_variant/<int:product_variant_id>/',views.delete_product_variant,name='delete_product_variant'),
    
    
    
    # Coupon Management
    
    path('coupon_manage/', views.coupon_manage, name='coupon_manage'),
    path("add_coupon/",views.add_coupon,name="add_coupon"),
    path("edit_coupon/<int:id>/",views.edit_coupon,name="edit_coupon"),
    path("delete_coupon/<int:id>/",views.delete_coupon,name="delete_coupon"),
    
    # path("soft_delete_coupon/<int:id>/",views.soft_delete_coupon,name="soft_delete_coupon"),
    # path("undelete_coupon/<int:id>/",views.undelete_coupon,name="undelete_coupon"),
    
    # Order Management
    
    path('order_list/',views.order_list,name='order_list'),
    path('order_details/<int:id>/', views.order_details, name="order_details"),
    path('cancel_order/',views.cancel_order,name='cancel_order'),
 
]