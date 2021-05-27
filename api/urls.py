from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/call_click/', views.call_click),
    path('register/', views.register, name='register'),
    path('api/buy_boost/', views.buy_boost),

]
