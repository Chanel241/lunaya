from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cycle
from .forms import CycleForm
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta

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
        elif cycle_day <= 14:
            phase = "Phase folliculaire"
        elif cycle_day <= 16:
            phase = "Ovulation"
        else:
            phase = "Phase lutéale"
        ovulation_date = latest_cycle.start_date + timedelta(days=14)
        next_period = latest_cycle.start_date + timedelta(days=cycle_length)
        cycle_info = {
            'cycle_day': cycle_day,
            'phase': phase,
            'ovulation_date': ovulation_date,
            'next_period': next_period
        }

        for cycle in cycles:
            days_since_start = (today - cycle.start_date).days + 1
            cycle_day = days_since_start % cycle.cycle_length if days_since_start > 0 else 1
            if cycle_day <= 5:
                phase = "Phase menstruelle"
            elif cycle_day <= 14:
                phase = "Phase folliculaire"
            elif cycle_day <= 16:
                phase = "Ovulation"
            else:
                phase = "Phase lutéale"
            cycles_with_phases.append({
                'cycle': cycle,
                'phase': phase,
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
            cycle.save()
            messages.success(request, "Cycle ajouté avec succès.")
            return redirect('cycle_tracker')
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier vos données.")
    else:
        form = CycleForm()
    return render(request, 'cycle/add.html', {'form': form})