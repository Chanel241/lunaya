from django import forms
from .models import Cycle

class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = ['start_date', 'end_date', 'cycle_length', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'cycle_length': forms.NumberInput(attrs={'min': 21, 'max': 35}),
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Notes sur votre cycle...'}),
        }