from django.urls import path
from . import views

urlpatterns = [
    path('', views.meditations_list, name='meditations_list'),
    path('create/', views.meditation_create, name='meditation_create'),
    path('delete/<int:pk>/', views.meditation_delete, name='meditation_delete'),
]