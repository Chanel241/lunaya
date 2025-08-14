from django import forms
from .models import Meditation

class MeditationForm(forms.ModelForm):
    class Meta:
        model = Meditation
        fields = ['title', 'description', 'audio_file']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'audio_file': 'Fichier audio',
        }