from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cercle
from .forms import CercleForm
from django.contrib import messages

@login_required
def community(request):
    posts = Cercle.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = CercleForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Votre message a été publié avec succès.")
            return redirect('community')
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier votre message.")
    else:
        form = CercleForm()
    return render(request, 'cercle/community.html', {'posts': posts, 'form': form})

@login_required
def cercle_add(request):
    if request.method == 'POST':
        form = CercleForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Votre message a été publié avec succès.")
            return redirect('community')
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier votre message.")
    else:
        form = CercleForm()
    return render(request, 'cercle/add.html', {'form': form})