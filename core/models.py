from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    language = models.CharField(max_length=10, choices=[('fr', 'Français'), ('fg', 'Fang')], default='fr')
    last_period = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profil de {self.user.username}"