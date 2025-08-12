from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cycle
from .forms import CycleForm
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from django.db import transaction

@login_required
def cycle_tracker(request):
    today = timezone.now().date()
    cycles = Cycle.objects.filter(user=request.user).order_by('-start_date')
    cycle_info = {}
    cycles_with_phases = []

    if cycles.exists():
        latest_cycle = cycles.first()
        days_since_start = (today - latest_cycle.start_date).days + 1
        cycle_length = latest_cycle.cycle_length or 28
        cycle_day = days_since_start % cycle_length if days_since_start > 0 else 1
        if cycle_day <= 5:
            phase = "Phase menstruelle"
            color = "red"
            article_topic = "Santé menstruelle"
        elif cycle_day <= 14:
            phase = "Phase folliculaire"
            color = "green"
            article_topic = "Hormones"
        elif cycle_day <= 16:
            phase = "Ovulation"
            color = "yellow"
            article_topic = "Fertilité"
        else:
            phase = "Phase lutéale"
            color = "blue"
            article_topic = "Contraception"
        ovulation_date = latest_cycle.start_date + timedelta(days=14)
        next_period = latest_cycle.start_date + timedelta(days=cycle_length)
        cycle_info = {
            'cycle_day': cycle_day,
            'phase': phase,
            'color': color,
            'ovulation_date': ovulation_date,
            'next_period': next_period,
            'article_topic': article_topic
        }

        for cycle in cycles:
            days_since_start = (today - cycle.start_date).days + 1
            cycle_day = days_since_start % cycle.cycle_length if days_since_start > 0 else 1
            if cycle_day <= 5:
                phase = "Phase menstruelle"
                color = "red"
            elif cycle_day <= 14:
                phase = "Phase folliculaire"
                color = "green"
            elif cycle_day <= 16:
                phase = "Ovulation"
                color = "yellow"
            else:
                phase = "Phase lutéale"
                color = "blue"
            cycles_with_phases.append({
                'cycle': cycle,
                'phase': phase,
                'color': color,
                'cycle_day': cycle_day
            })

    if request.method == 'POST':
        form = CycleForm(request.POST)
        if form.is_valid():
            cycle = form.save(commit=False)
            cycle.user = request.user
            cycle.save()
            messages.success(request, "Cycle enregistré avec succès.")
            return redirect('cycle_tracker')
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier vos données.")
    else:
        form = CycleForm()
    return render(request, 'cycle/tracker.html', {
        'form': form,
        'cycles': cycles_with_phases,
        'cycle_info': cycle_info
    })

@login_required
def cycle_add(request):
    if request.method == 'POST':
        form = CycleForm(request.POST)
        if form.is_valid():
            cycle = form.save(commit=False)
            cycle.user = request.user
            try:
                with transaction.atomic():
                    cycle.save()
                messages.success(request, "Cycle ajouté avec succès.")
                return redirect('cycle_tracker')
            except Exception as e:
                messages.error(request, f"Erreur lors de l'enregistrement : {str(e)}")
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier vos données.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = CycleForm()
    return render(request, 'cycle/add.html', {'form': form})

@login_required
def article_view(request, topic):
    articles = {
        'sante-menstruelle': "Conseils pour gérer les douleurs menstruelles avec des infusions et du repos.",
        'hormones': "Comprendre les fluctuations hormonales pendant la phase folliculaire.",
        'fertilite': "Astuces pour optimiser la fertilité pendant l’ovulation.",
        'contraception': "Options de contraception adaptées à la phase lutéale."
    }
    content = articles.get(topic, "Article non disponible.")
    return render(request, 'cycle/article.html', {'topic': topic, 'content': content})

@login_required
def cycle_clear_history(request):
    if request.method == "POST":
        Cycle.objects.filter(user=request.user).delete()
        messages.success(request, "L'historique a été supprimé avec succès.")
        return redirect('cycle_tracker')
    return redirect('cycle_tracker')

@login_required
def cycle_delete_entry(request, cycle_id):
    if request.method == "POST":
        cycle = Cycle.objects.get(id=cycle_id, user=request.user)
        cycle.delete()
        messages.success(request, "L'enregistrement a été supprimé avec succès.")
        return redirect('cycle_tracker')
    return redirect('cycle_tracker')