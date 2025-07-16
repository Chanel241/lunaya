from django.urls import path
from . import views

urlpatterns = [
    path('', views.wellness_list, name='wellness_list'),
    path('tip/<int:tip_id>/', views.wellness_detail, name='wellness_detail'),
]