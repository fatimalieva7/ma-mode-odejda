from django.shortcuts import render

def index(request):
    return render(request, 'market/index.html')

def checkout(request):
    return render(request, 'market/checkout.html')

def contact(request):
    return render(request, 'market/contact.html')

def shop_details(request):
    return render(request, 'market/shop-details.html')

def shoping_cart(request):
    return render(request, 'market/shoping-cart.html')
def shop_grid(request):
    return render(request, 'market/shop-grid.html')
