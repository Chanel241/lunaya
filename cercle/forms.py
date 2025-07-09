from django import forms
from .models import Cercle

class CercleForm(forms.ModelForm):
    class Meta:
        model = Cercle
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Partagez vos pensées...'}),
        }