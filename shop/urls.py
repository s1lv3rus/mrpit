from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('objective/<slug:objective_slug>/', views.objective_list, name='objective_list'),
    path('search/', views.search, name='search_results'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('supplier/<int:supplier_id>/', views.product_list_by_supplier_id, name='product_list_by_supplier'),
    path('supplier/<slug:supplier_slug>/', views.product_list_by_supplier, name='product_list_by_supplier'),
    path('category/<int:category_id>/', views.product_list_by_category_id, name='product_list_by_category'),
    path('category/<slug:category_slug>/', views.product_list_by_category, name='product_list_by_category'),
    path('index/', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('payment/', views.payment, name='payment'),
    path('faq/', views.faq, name='faq'),
    path('news/', views.news, name='news'),
    path('certificate/', views.certificate, name='certificate'),
    path('feedback/', views.feedback, name='feedback'),
    path('thanks/', views.thanks, name='thanks'),
    path('articles/', views.articles, name='articles'),
    path('articles/<slug:article_slug>/', views.article, name='article'),
    path('delivery/', views.delivery, name='delivery'),
    path('', views.product_list, name='product_list'),
]

