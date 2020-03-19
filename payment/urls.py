from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('notifications/', views.notifications, name='notifications'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('process/<int:order_id>/', views.payment_process, name='process'),
]