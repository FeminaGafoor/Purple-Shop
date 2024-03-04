from django.urls import path
from . import views


app_name='shop_app'   

urlpatterns = [

# products view-----------

    path('',views.shop,name='shop'),
    path('category/<slug:category_slug>/', views.shop, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>', views.single_product, name='single_product'),
    path('search/',views.search,name='search'),
    path('get_product_suggestions/', views.get_product_suggestions, name='get_product_suggestions'),
    path('filter/',views.filter,name='filter'),
    path('contact/',views.contact,name='contact')
   


]
    