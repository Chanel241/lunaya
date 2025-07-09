
from django.db import models

class WellnessTip(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=[
        ('yoga', 'Yoga'),
        ('tea', 'Thé Apaisant'),
        ('relaxation', 'Relaxation'),
    ])
    date = models.DateField(null=True, blank=True)  # Nouveau champ pour les conseils quotidiens
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('type', 'date')  # Un conseil par type et par jour