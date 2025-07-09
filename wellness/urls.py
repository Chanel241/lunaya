from django.urls import path
from . import views

urlpatterns = [
    path('', views.wellness_list, name='wellness_list'),
]