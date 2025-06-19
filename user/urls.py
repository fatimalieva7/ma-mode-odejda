from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    # Страница товаров определенной категории (со слагом)
    path('checkout/', views.checkout, name='checkout'),
    path('process-order/', views.process_order, name='process-order'),
    path('order-success/', views.order_success, name='success'),
    path('login/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('send-message/', views.message_sent, name='message_send'),

]