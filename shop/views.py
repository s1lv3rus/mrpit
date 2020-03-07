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


def product_list(request, category_slug=None, supplier_id=None):
    [categories, suppliers, objectives, products_rec, offers] = list()
    template = 'shop/index.html'
    context = locals()
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
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(subject, message, sender, ['admin@mrpit.online'])
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
