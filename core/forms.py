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
        choices=[('fr', 'Français'), ('fg', 'Fang')],
        required=True,
        label="Langue"
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'birthdate', 'last_period', 'language']