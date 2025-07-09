from django.db import models
from django.contrib.auth.models import User

class Cycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    cycle_length = models.IntegerField(default=28, help_text="Durée moyenne du cycle en jours (21-35)")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cycle de {self.user.username} du {self.start_date}"