from django.urls import path
from . import views

urlpatterns = [
    path('', views.cycle_tracker, name='cycle_tracker'),
    path('add/', views.cycle_add, name='cycle_add'),
    path('article/<slug:topic>/', views.article_view, name='article'),
    path('clear_history/', views.cycle_clear_history, name='cycle_clear_history'),
    path('delete_entry/<int:cycle_id>/', views.cycle_delete_entry, name='cycle_delete_entry'),
]