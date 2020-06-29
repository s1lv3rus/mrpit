from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import *
from orders.models import *
from .forms import *
from .models import Profile
from django.contrib.auth import logout
from shop.views import list


def user_login(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('cart:cart_detail')
                else:
                    messages.error(request, 'Аккаунт неактивен!')
                    context = locals()
                    template = 'account/login.html'
                    return render(request, template, context)
            else:
                messages.error(request, 'Неверные логин или пароль')
                context = locals()
                template = 'account/login.html'
                return render(request, template, context)
    else:
        form = LoginForm()
    context = locals()
    template = 'account/login.html'
    return render(request, template, context)


def user_logout(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    logout(request)
    context = locals()
    template = 'account/logged_out.html'
    return render(request, template, context)


def register(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            email = user_form.cleaned_data["email"]
            # проверка на наличие email в базе. Уникальное значение в базе не удалось проставить
            if User.objects.filter(email=email).count() > 0 and email:
                messages.error(request, 'Пользовать с указанным email уже существует')
                context = locals()
                template = 'account/register.html'
                return render(request, template, context)
            else:
                new_user.save()
                login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Спасибо за регистрацию на нашем сайте!')
                context = locals()
                return redirect('cart:cart_detail')
    else:
        user_form = UserRegistrationForm()
    context = locals()
    template = 'account/register.html'
    return render(request, template, context)


@login_required
def profile(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    orders = Order.published.filter(client=request.user)
    # Если юзер авторизован, то находим его профиль иначе редиректим на форму входа на сайт
    if request.user.is_authenticated:
        profile = Profile.published.get(user=request.user)
    else:
        return redirect('login')

    # блок для редактирования профиля
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Профиль успешно изменён')
    else:
        user_form = UserProfileForm(instance=profile)
    context = locals()
    template = 'account/profile.html'
    return render(request, template, context)
