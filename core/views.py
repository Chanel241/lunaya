from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, ProfileForm
from .models import Profile
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/password_reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain'] = settings.DOMAIN
        context['protocol'] = 'https'
        context['site_name'] = settings.SITE_NAME
        context['uidb64'] = kwargs.get('uidb64', '')  
        context['token'] = kwargs.get('token', '')   
        return context
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile_data = {
                'birthdate': form.cleaned_data['birthdate'],
                'language': form.cleaned_data['language'],
                'last_period': form.cleaned_data['last_period']
            }
            Profile.objects.update_or_create(user=user, defaults=profile_data)
            login(request, user)
            messages.success(request, "Inscription réussie ! Bienvenue sur Lunaya.")
            return redirect('home')
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier les champs ci-dessous.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form[field].label}: {error}")
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
                    return redirect(next_url)  
                except Exception:
                    pass 
            return redirect(reverse('home'))  
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

@login_required  
def profile_edit(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/profile.html', {'profile': profile, 'editing': True, 'form': form})

@require_POST
@csrf_exempt  
def toggle_offline_mode(request):
    if request.method == 'POST':
        try:
            data = request.POST if request.POST else json.loads(request.body.decode('utf-8'))
            offline_mode = data.get('offline_mode', False)
            request.session['offline_mode'] = bool(offline_mode)
            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'success': False}, status=400)