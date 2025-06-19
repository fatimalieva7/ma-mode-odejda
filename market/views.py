
from django.shortcuts import render, get_object_or_404
from .models import Image, ProductClothing, CategoryClothing, ContactMessage
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
import random
from django.contrib.auth import authenticate, login, logout
from .forms import  UserRegisterForm
from django.contrib.auth.models import User
from django.db.models import Q



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



def get_cart(request):
    """Получаем или создаем корзину в сессии"""
    cart = request.session.get('cart', {})
    return cart


def save_cart(request, cart):
    """Сохраняем корзину в сессии"""
    request.session['cart'] = cart
    request.session.modified = True


def shop_grid(request, slug=None):
    categories = CategoryClothing.objects.all()

    if slug:
        category = get_object_or_404(CategoryClothing, slug=slug)
        products = ProductClothing.objects.filter(category=category)
    else:
        products = ProductClothing.objects.all()

    return render(request, 'market/shop-grid.html', {
        'categories': categories,
        'products': products,
        'current_category_slug': slug,  # Передаем текущий категорий в шаблон

    })


def shop_details(request, slug):
    product = get_object_or_404(ProductClothing, slug=slug)
    related_products = ProductClothing.objects.exclude(slug=slug)[:4]

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size')
        color = request.POST.get('color')

        # Логика добавления в корзину
        cart = get_cart(request)
        product_key = f"{product.id}_{size}_{color}" if size or color else str(product.id)

        if product_key in cart:
            cart[product_key]['quantity'] += quantity
        else:
            cart[product_key] = {
                'product_id': product.id,
                'name': product.name,
                'price': str(product.price),
                'image': product.image.url,
                'quantity': quantity,
                'size': size,
                'color': color
            }

        save_cart(request, cart)
        messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
        return redirect('market:shop-details', slug=slug)

    return render(request, 'market/shop-details.html', {
        'product': product,
        'related_products': related_products
    })


def add_to_cart_from_grid(request, product_id):
    """Добавление товара в корзину из сетки товаров (по иконке корзины)"""
    product = get_object_or_404(ProductClothing, id=product_id)

    cart = get_cart(request)
    product_key = str(product.id)  # Без размера и цвета при добавлении из сетки

    if product_key in cart:
        cart[product_key]['quantity'] += 1
    else:
        cart[product_key] = {
            'product_id': product.id,
            'name': product.name,
            'price': str(product.price),
            'image': product.image.url,
            'quantity': 1,
            'size': None,
            'color': None
        }

    save_cart(request, cart)
    messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
    return redirect('market:shop-grid')


def shoping_cart(request):
    cart = get_cart(request)
    cart_items = []
    subtotal = 0

    for key, item in cart.items():
        # Создаем объект "элемент корзины" для удобного отображения
        cart_item = {
            'product': {
                'id': item['product_id'],
                'name': item['name'],
                'price': float(item['price']),
                'image': item['image']
            },
            'quantity': item['quantity'],
            'size': item.get('size'),
            'color': item.get('color'),
            'total': float(item['price']) * item['quantity']
        }
        cart_items.append(cart_item)
        subtotal += cart_item['total']

    total = subtotal  # Здесь можно добавить расчет доставки и т.д.

    return render(request, 'market/shoping-cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total
    })


def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = get_cart(request)

        # Находим товар в корзине (первое вхождение с таким product_id)
        product_key = next((key for key in cart.keys() if str(product_id) in key), None)

        if product_key:
            if quantity > 0:
                cart[product_key]['quantity'] = quantity
            else:
                del cart[product_key]

            save_cart(request, cart)
            messages.success(request, 'Корзина обновлена')

    return redirect('market:shoping-cart')


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = get_cart(request)

        # Находим и удаляем товар из корзины
        product_key = next((key for key in cart.keys() if str(product_id) in key), None)

        if product_key:
            del cart[product_key]
            save_cart(request, cart)
            messages.success(request, 'Товар удален из корзины')

    return redirect('market:shoping-cart')




@require_POST
def process_order(request):
    # Получаем данные формы
    form_data = {
        'first_name': request.POST.get('first_name'),
        'last_name': request.POST.get('last_name'),
        'email': request.POST.get('email'),
        'phone': request.POST.get('phone'),
        'country': request.POST.get('country'),
        'city': request.POST.get('city'),
        'address': request.POST.get('address'),
        'postcode': request.POST.get('postcode'),
        'notes': request.POST.get('notes'),
    }

    # Генерируем информацию о заказе
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    delivery_date = (datetime.now() + timedelta(days=3)).strftime("%d %B %Y")

    # Сохраняем данные в сессии
    request.session['order_success_data'] = {
        **form_data,
        'order_number': order_number,
        'delivery_date': delivery_date,
        'payment_method': 'Наличными при получении',
        'total': request.session.get('cart_total', 0)
    }

    # Здесь можно добавить сохранение заказа в базу данных

    return redirect('market:order-success')


def order_success(request):
    order_data = request.session.get('order_success_data')

    if not order_data:
        return redirect('market:checkout')

    context = {
        'order_number': order_data['order_number'],
        'delivery_date': order_data['delivery_date'],
        'payment_method': order_data['payment_method'],
        'total': order_data['total'],
        'customer_name': f"{order_data['first_name']} {order_data['last_name']}",
        'email': order_data['email'],
        'address': f"{order_data['country']}, {order_data['city']}, {order_data['address']}, {order_data['postcode']}"
    }

    # Очищаем корзину после оформления
    if 'cart' in request.session:
        del request.session['cart']

    return render(request, 'market/success.html', context)
def register(request):
    if request.method == 'POST':
        form_register_user = UserRegisterForm(request.POST)
        if form_register_user.is_valid():
            username = form_register_user.cleaned_data['username']
            email = form_register_user.cleaned_data['email']
            password = form_register_user.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                form_register_user.add_error('username', 'Пользователь с таким именем уже существует.')

            elif User.objects.filter(email=email).exists():
                form_register_user.add_error('email', 'Пользователь с таким email уже существует.')

            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                user.save()
                authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('market:index')

    else:
        form_register_user = UserRegisterForm()

    context = {'form_register_user': form_register_user}
    return render(request, 'market/register.html', context)



def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        # Ищем в названии и описании товара
        results = ProductClothing.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    return render(request, 'market/search.html', {
        'results': results,
        'query': query
    })


def send_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        # Сохраняем сообщение в базу
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        # Отправка email (дополнительно)
        try:
            from django.core.mail import send_mail
            send_mail(
                f'New message from {name}',
                message_text,
                email,
                ['your@email.com'],  # Ваш email для уведомлений
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email sending error: {e}")

        messages.success(request, 'Your message has been sent successfully!')
        return redirect(request.META.get('HTTP_REFERER', 'market:home'))

    return redirect('market:index')
def logout_view(request):
    logout(request)
    return redirect('market:index')

def checkout(request):
    return render(request, 'market/checkout.html')
def contact(request):
    return render(request, 'market/contact.html')


def message_sent(request):
    return render(request, 'market/message_send.html')
