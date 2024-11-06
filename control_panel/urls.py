# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('run-pokebot/', views.run_pokebot, name='run_pokebot'),
]
