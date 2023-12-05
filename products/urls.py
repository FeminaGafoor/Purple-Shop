from django.urls import path
from . import views


app_name='shop_app'   

urlpatterns = [

    path('',views.shop,name='shop'),
    path('<slug:category_slug>/', views.shop, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>', views.single_product, name='single_product'),
   
]
    