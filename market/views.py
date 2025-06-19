from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import Image, ProductClothing, CategoryClothing
from django.contrib import messages

def index(request):
    images = Image.objects.all()
    # Используем ProductClothing вместо ProductIndex
    products = ProductClothing.objects.order_by('-created_at')[:6]
    return render(request, 'market/index.html', {
        'images': images,
        'products': products
    })
def category(request,slug):
    category_slug = CategoryClothing.objects.all()
    categori = get_object_or_404(CategoryClothing, slug=slug)
    products = ProductClothing.objects.filter(category=categori)
    return render(request, 'market/category.html', {'categori': categori, 'category_slug': category_slug, 'products': products})



def shop_grid(request, slug=None):
    categories = CategoryClothing.objects.all()
    
    if slug:
        # Если передан slug категории, фильтруем товары по категории
        category = get_object_or_404(CategoryClothing, slug=slug)
        products = ProductClothing.objects.filter(category=category)
    else:
        # Иначе показываем все товары
        products = ProductClothing.objects.all()
    
    return render(request, 'market/shop-grid.html', {
        'categories': categories,
        'products': products,
        'current_category_slug': slug  # Для подсветки активной категории в шаблоне
    })


def shop_details(request, slug):
    product = get_object_or_404(ProductClothing, slug=slug)
    related_products = ProductClothing.objects.exclude(slug=slug)[:4]

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size')
        color = request.POST.get('color')

        # Здесь должна быть логика добавления в корзину
        # Например, используя сессии или модель Cart
        messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
        return redirect('market:shop-details', slug=slug)

    return render(request, 'market/shop-details.html', {
        'product': product,
        'related_products': related_products
    })
def shoping_cart(request):
    return render(request, 'market/shoping-cart.html')

def checkout(request):
    return render(request, 'market/checkout.html')

def contact(request):
    return render(request, 'market/contact.html')


