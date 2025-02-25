from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='services_list'),
    path('create/', views.create, name='services_create'),
    path('<int:id>/', views.index, name='index'),
    path('<int:id>/request_service/', views.request_service, name='request_service'),
    path('<slug:field>/', views.service_field, name='services_field'),
]
