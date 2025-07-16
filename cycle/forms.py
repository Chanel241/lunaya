from django import forms
from .models import Cycle

class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = ['start_date', 'end_date', 'cycle_length', 'notes', 'pain', 'mood', 'appetite', 'energy', 'libido']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'cycle_length': forms.NumberInput(attrs={'min': 21, 'max': 35}),
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Notes sur votre cycle...'}),
            'pain': forms.NumberInput(attrs={'min': 0, 'max': 10, 'placeholder': 'Douleur (0-10)'}),
            'mood': forms.NumberInput(attrs={'min': 0, 'max': 10, 'placeholder': 'Humeur (0-10)'}),
            'appetite': forms.NumberInput(attrs={'min': 0, 'max': 10, 'placeholder': 'Appétit (0-10)'}),
            'energy': forms.NumberInput(attrs={'min': 0, 'max': 10, 'placeholder': 'Énergie (0-10)'}),
            'libido': forms.NumberInput(attrs={'min': 0, 'max': 10, 'placeholder': 'Libido (0-10)'}),
        }
        labels = {
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'cycle_length': 'Durée du cycle (jours)',
            'notes': 'Notes',
            'pain': 'Douleur',
            'mood': 'Humeur',
            'appetite': 'Appétit',
            'energy': 'Énergie',
            'libido': 'Libido',
        }