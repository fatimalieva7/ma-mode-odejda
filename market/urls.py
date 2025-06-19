from django.urls import path
from . import views



app_name = 'market'


urlpatterns = [
    path('', views.index, name='index'),
    path('shop-grid/', views.shop_grid, name='shop-grid'),
    # Страница товаров определенной категории (со слагом)
    path('shop-grid/<slug:slug>/', views.shop_grid, name='shop-category'),
    path('product/<slug:slug>/', views.shop_details, name='shop-details'),
    # Корзина
    path('cart/', views.shoping_cart, name='shoping-cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_from_grid, name='add-to-cart-grid'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update-cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('search/', views.search, name='search'),


]