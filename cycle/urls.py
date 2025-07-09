from django.urls import path
from . import views

urlpatterns = [
    path('', views.cycle_tracker, name='cycle_tracker'),
    path('add/', views.cycle_add, name='cycle_add'),
]