from django.urls import path, re_path
from . import views
from .views import YandexNotifications

app_name = 'payment'

urlpatterns = [
    path('notifications/', YandexNotifications.as_view(), name='notifications'),
    path('process/<int:order_id>/', views.payment_process, name='process'),
]
