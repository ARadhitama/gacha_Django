from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('spin/', views.spin_gacha, name='spin'),
    path('spin_history/', views.spin_history, name='history'),
]