from django.urls import path
from . import views

urlpatterns = [
    path('', views.community, name='community'),
    path('add/', views.cercle_add, name='cercle_add'),
]