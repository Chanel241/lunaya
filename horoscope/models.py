
from django.db import models

class Horoscope(models.Model):
    sign = models.CharField(max_length=20, choices=[
        ('aries', 'Bélier'), ('taurus', 'Taureau'), ('gemini', 'Gémeaux'),
        ('cancer', 'Cancer'), ('leo', 'Lion'), ('virgo', 'Vierge'),
        ('libra', 'Balance'), ('scorpio', 'Scorpion'), ('sagittarius', 'Sagittaire'),
        ('capricorn', 'Capricorne'), ('aquarius', 'Verseau'), ('pisces', 'Poissons')
    ])
    date = models.DateField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sign} - {self.date}"

    class Meta:
        unique_together = ['sign', 'date']