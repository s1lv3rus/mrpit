from itertools import chain

from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from .models import *
from cart.forms import CartAddProductForm
from cart.views import cart_add
from django.views.generic import ListView
from django.template import RequestContext

from account.models import Profile


def list():
    categories = Category.published.all()
    suppliers = Supplier.published.all()
    objectives = Objective.published.all()
    products_rec = Product.published.filter(recommendation=True)
    offers = Offer.published.all()
    return [categories, suppliers, objectives, products_rec, offers]


def search(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    query = request.GET.get('q')
    object_list = Product.published.filter(Q(name__icontains=query) | Q(description__icontains=query))
    context = locals()
    template = 'shop/product/search.html'
    return render(request, template, context)


def product_list_by_category(request, category_slug):
    [categories, suppliers, objectives, products_rec, offers] = list()
    category = Category.published.get(slug=category_slug)
    subcategories = Category.published.get(slug=category_slug).subcategories.all()
    template = 'shop/product/products_by_category.html'
    context = locals()
    return render(request, template, context)


def product_list_by_category_id(request, category_id):
    [categories, suppliers, objectives, products_rec, offers] = list()
    category = Category.published.get(id=category_id)
    subcategories = Category.published.get(id=category_id).subcategories.all()
    template = 'shop/product/products_by_category.html'
    context = locals()
    return render(request, template, context)


def product_list_by_supplier(request, supplier_slug):
    [categories, suppliers, objectives, products_rec, offers] = list()
    supplier = Supplier.published.get(slug=supplier_slug)
    products = supplier.products_s.all()
    template = 'shop/product/products_by_supplier.html'
    context = locals()
    return render(request, template, context)


def product_list_by_supplier_id(request, supplier_id):
    [categories, suppliers, objectives, products_rec, offers] = list()
    supplier = Supplier.published.get(id=supplier_id)
    products = supplier.products_s.all()
    template = 'shop/product/products_by_supplier.html'
    context = locals()
    return render(request, template, context)


def product_detail(request, slug):
    [categories, suppliers, objectives, products_rec, offers] = list()
    product = Product.published.get(slug=slug)
    comments = product.comments.all()
    count = product.comments.all().count
    flavours = product.flavours.all()
    cart_product_form = CartAddProductForm()

    if request.method == 'POST':
        form = AddComment(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.product = product
            new_comment.save()
    else:
        form = AddComment()

    template = 'shop/product/detail.html'
    context = locals()
    return render(request, template, context)


def objective_list(request, objective_slug):
    [categories, suppliers, objectives, products_rec, offers] = list()
    objective = Objective.published.get(slug=objective_slug)
    categories_p = Objective.published.get(slug=objective_slug).categories.all()
    offers = objective.offers.all()
    template = 'shop/product/objective_list.html'
    context = locals()
    return render(request, template, context)


def index(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    context = locals()
    template = 'shop/index.html'
    return render(request, template, context)


def info(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    template = 'shop/info.html'
    context = locals()
    return render(request, template, context)


def delivery(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    template = 'shop/delivery.html'
    context = locals()
    return render(request, template, context)


def payment(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    template = 'shop/payment.html'
    context = locals()
    return render(request, template, context)


def feedback(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # Если форма заполнена корректно, сохраняем все введённые пользователем значения
        if form.is_valid():
            name = form.cleaned_data['name']
            sender = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(name, message, sender, ['admin@mrpit.online'])
            # Переходим на другую страницу, если сообщение отправлено
            return redirect('shop:thanks')
    else:
        form = ContactForm()
    template = 'shop/feedback.html'
    context = locals()
    return render(request, template, context)


def thanks(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    template = 'shop/thanks.html'
    context = locals()
    return render(request, template, context)


def faq(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    template = 'shop/faq.html'
    context = locals()
    return render(request, template, context)


def articles(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    articles = Article.published.all()
    template = 'shop/articles/articles.html'
    context = locals()
    return render(request, template, context)


def article(request, article_slug):
    [categories, suppliers, objectives, products_rec, offers] = list()
    article = Article.published.get(slug=article_slug)
    template = 'shop/articles/article.html'
    context = locals()
    return render(request, template, context)


def certificate(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    template = 'shop/certificate.html'
    context = locals()
    return render(request, template, context)


def news(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    news = News.published.all()
    template = 'shop/news.html'
    context = locals()
    return render(request, template, context)


def page_not_found(request, exception):
    [categories, suppliers, objectives, products_rec, offers] = list()
    template = 'shop/404.html'
    status = 404
    context = locals()
    return render(request, template, context)


def page_not_found_500(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    template = 'shop/500.html'
    status = 500
    context = locals()
    return render(request, template, context)


def calc(request):
    [categories, suppliers, objectives, products_rec, offers] = list()
    if request.method == 'POST':
        form = CalcForm(request.POST)
        # Если форма заполнена корректно, сохраняем все введённые пользователем значения
        if form.is_valid():
            sex = form.cleaned_data['sex']
            year = form.cleaned_data['year']
            height = form.cleaned_data['height']
            body_mass = form.cleaned_data['body_mass']
            number_of_meals = form.cleaned_data['number_of_meals']
            objective = form.cleaned_data['objective']
            client_year = None
            client_height = None
            number_of_meals = None
            client_body_mass = 0

            if 25 <= year <= 40:
                client_year = 'ЦА'
            elif year < 25:
                client_year = 'Меньше 25'
            elif year > 40:
                client_year = 'Больше 40'

            if 160 <= height <= 180:
                client_height = 'Средний'
            elif height > 180:
                client_height = 'Высокий'
            elif height < 160:
                client_height = 'Низкий'

            if body_mass <= 60:
                client_body_mass = 'Худой'
            elif 60 < body_mass <= 75:
                client_body_mass = 'Средний'
            elif 76 < body_mass <= 90:
                client_body_mass = 'Упитанный'
            elif body_mass > 91:
                client_body_mass = 'Большой'

            if sex == 'муж':
                client_sex = 'мужской'
                bum = 66 + (13.7 * body_mass) + (5 * height) - (6.8 * year)

            else:
                client_sex = 'женский'
                bum = 655 + (9.6 * body_mass) + (1.8 * height) - (4.7 * year)
            calories_day = int(bum * 1.5)

            if client_year == 'ЦА' and client_height == 'Средний' and objective == 'Набрать массу' and client_body_mass != 'Худой':
                client_offer = Offer.published.get(calc='ЦСНС')
            if client_year == 'ЦА' and client_height == 'Средний' and objective == 'Набрать массу' and client_body_mass == 'Худой':
                client_offer = Offer.published.get(calc='ЦСНХ')
            if client_year == 'ЦА' and client_height == 'Средний' and objective == 'Похудеть' and client_body_mass != 'Худой':
                client_offer = Offer.published.get(calc='ЦСПС')
            if client_year == 'ЦА' and client_height == 'Средний' and objective == 'Похудеть' and client_body_mass == 'Худой':
                client_offer = Offer.published.get(calc='ЦСПХ')

            template = 'shop/calc/completed.html'
            context = locals()
            return render(request, template, context)
    else:
        form = CalcForm()
    template = 'shop/calc/calc.html'
    context = locals()
    return render(request, template, context)
