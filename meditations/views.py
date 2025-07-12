from django.shortcuts import render
from .models import Meditation

def meditations_list(request):
    meditations = Meditation.objects.all().order_by('title')
    return render(request, 'meditations/list.html', {'meditations': meditations})