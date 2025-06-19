from django.urls import path
from . import views



app_name = 'market'


urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    
    # Страница категорий товаров (без слага)
    path('shop-grid/', views.shop_grid, name='shop-grid'),
    # Страница товаров определенной категории (со слагом)
    path('shop-grid/<slug:slug>/', views.shop_grid, name='shop-category'),
    # Детали товара
    path('shop-details/<slug:slug>/', views.shop_details, name='shop-details'),
    # Корзина
    path('cart/', views.shoping_cart, name='shoping-cart'),
]