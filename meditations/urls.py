from django.urls import path
from . import views

urlpatterns = [
    path('', views.meditation_list, name='meditation_list'),
    path('create/', views.meditation_create, name='meditation_create'),
    path('delete/<int:pk>/', views.meditation_delete, name='meditation_delete'),
]