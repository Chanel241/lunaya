from django.db import models
from django.contrib.auth.models import User

class Cycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    cycle_length = models.IntegerField(default=28, help_text="Durée moyenne du cycle en jours (21-35)")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Champs pour les symptômes
    pain = models.IntegerField(choices=[(i, str(i)) for i in range(11)], null=True, blank=True, help_text="Douleur (0-10)")
    mood = models.IntegerField(choices=[(i, str(i)) for i in range(11)], null=True, blank=True, help_text="Humeur (0-10)")
    appetite = models.IntegerField(choices=[(i, str(i)) for i in range(11)], null=True, blank=True, help_text="Appétit (0-10)")
    energy = models.IntegerField(choices=[(i, str(i)) for i in range(11)], null=True, blank=True, help_text="Énergie (0-10)")
    libido = models.IntegerField(choices=[(i, str(i)) for i in range(11)], null=True, blank=True, help_text="Libido (0-10)")

    def __str__(self):
        return f"Cycle de {self.user.username} du {self.start_date}"