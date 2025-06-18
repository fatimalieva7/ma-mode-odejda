from django.urls import path
from . import views



app_name = 'market'


urlpatterns = [
    path('', views.index, name='index'),
    path('shop-details/', views.shop_details, name='shop-details'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('shoping-cart/', views.shoping_cart, name='shoping-cart'),
    path('shop-grid/', views.shop_grid, name='shop-grid'),
]