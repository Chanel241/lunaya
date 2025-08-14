from django.shortcuts import render, redirect
from .models import Meditation
from .forms import MeditationForm
from django.contrib.auth.decorators import login_required

@login_required
def meditation_list(request):
    meditations = Meditation.objects.filter(audio_file__isnull=False)
    return render(request, 'meditations/list.html', {'meditations': meditations})

@login_required
def meditation_create(request):
    if request.method == 'POST':
        form = MeditationForm(request.POST, request.FILES)
        if form.is_valid():
            meditation = form.save(commit=False)
            meditation.user = request.user
            meditation.save()
            return redirect('meditation_list')
    else:
        form = MeditationForm()
    return render(request, 'meditations/create.html', {'form': form})

@login_required
def meditation_delete(request, pk):
    meditation = Meditation.objects.get(id=pk)
    if request.user == meditation.user:
        meditation.delete()
    return redirect('meditation_list')