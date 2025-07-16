from django.db import models

class WellnessTip(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=[
        ('yoga', 'Yoga'),
        ('tea', 'Thé Apaisant'),
        ('relaxation', 'Relaxation'),
    ])
    date = models.DateField(null=True, blank=True)  #
    created_at = models.DateTimeField(auto_now_add=True)
    steps = models.TextField(blank=True, help_text="Étapes détaillées pour suivre le conseil")
    duration = models.CharField(max_length=50, blank=True, help_text="Durée approximative (ex. 10 minutes)")
    benefits = models.TextField(blank=True, help_text="Bienfaits du conseil")

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('type', 'date')  