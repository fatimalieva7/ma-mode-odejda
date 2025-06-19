
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
import random
from django.contrib.auth import authenticate, login, logout
from .forms import  UserRegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ContactMessage







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

    return redirect('user:success')


def order_success(request):
    order_data = request.session.get('order_success_data')

    if not order_data:
        return redirect('user:checkout')

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

    return render(request, 'user/success.html', context)
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
    return render(request, 'user/register.html', context)
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
    return render(request, 'user/checkout.html')
def contact(request):
    return render(request, 'user/contact.html')


def message_sent(request):
    return render(request, 'user/message_send.html')
