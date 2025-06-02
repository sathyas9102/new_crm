from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('move_customer/', views.move_customer, name='move_customer'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('record_call/<int:customer_id>/', views.record_call, name='record_call'),
    path('call_history/<int:customer_id>/', views.call_history, name='call_history'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('bulk_mail/', views.bulk_mail_view, name='bulk_mail'),
    path('bulk_whatsapp/', views.bulk_whatsapp_view, name='bulk_whatsapp'),
]
