from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Meditation
from .forms import MeditationForm

def meditations_list(request):
    meditations = Meditation.objects.all().order_by('title')
    return render(request, 'meditations/list.html', {'meditations': meditations})

@login_required
def meditation_create(request):
    if request.method == 'POST':
        form = MeditationForm(request.POST, request.FILES)
        if form.is_valid():
            meditation = form.save(commit=False)
            meditation.user = request.user
            meditation.save()
            return redirect('meditations_list')
    else:
        form = MeditationForm()
    return render(request, 'meditations/create.html', {'form': form})

@login_required
def meditation_delete(request, pk):
    meditation = Meditation.objects.get(id=pk)
    if request.user == meditation.user:
        if request.method == 'POST':
            meditation.delete()
            return redirect('meditations_list')
        return render(request, 'meditations/confirm_delete.html', {'meditation': meditation})
    else:
        return redirect('meditations_list') 