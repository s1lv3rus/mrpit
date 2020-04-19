from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:flavour_id>/', views.cart_add, name='cart_add'),
    path('add_offer/<int:offer_id>/', views.add_offer, name='add_offer'),
    path('add_gift/', views.add_gift, name='add_gift'),
    path('remove/<int:flavour_id>/', views.cart_remove, name='cart_remove'),
    path('', views.cart_detail, name='cart_detail'),
]