from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Date de naissance"
    )
    last_period = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Date des dernières règles"
    )
    language = forms.ChoiceField(
        choices=[
            ('fr', 'Français'),
            ('en', 'Anglais'),
            ('de', 'Allemand'),
            ('es', 'Espagnol'),
            ('pt', 'Portugais'),
        ],
        required=True,
        label="Langue"
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'birthdate', 'last_period', 'language']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birthdate', 'language', 'last_period']
        labels = {
            'birthdate': 'Date de naissance',
            'language': 'Langue',
            'last_period': 'Date des dernières règles',
        }