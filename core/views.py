from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from .models import Profile
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                birthdate=form.cleaned_data['birthdate'],
                language=form.cleaned_data['language'],
                last_period=form.cleaned_data['last_period']
            )
            login(request, user)
            messages.success(request, "Inscription réussie ! Bienvenue sur Lunaya.")
            return redirect('home')
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier vos informations.")
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next')
            if next_url:
                try:
                    return redirect(next_url)  # Redirige vers l'URL demandée
                except Exception:
                    pass  # Passe si l'URL est invalide
            return redirect(reverse('home'))  # Redirige vers home par défaut
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = AuthenticationForm()
    next_url = request.GET.get('next', reverse('home'))
    return render(request, 'core/login.html', {'form': form, 'next': next_url})

def logout_view(request):
    logout(request)
    messages.success(request, "Déconnexion réussie.")
    return redirect('home')

def home(request):
    today = timezone.now()
    cycle_day = (today.day % 28) + 1
    moon_phase = (today.day % 30) // 4
    affirmations = [
        "Je suis en harmonie avec mon cycle.",
        "Mon énergie féminine rayonne.",
        "Je m’ancre dans la sagesse de mes ancêtres."
    ]
    context = {
        'cycle_day': cycle_day,
        'moon_phase': moon_phase,
        'affirmation': affirmations[today.day % len(affirmations)],
    }
    return render(request, 'core/home.html', context)

def profile(request):
    profile = Profile.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    return render(request, 'core/profile.html', {'profile': profile})