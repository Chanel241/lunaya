from django.db import models
from django.conf import settings

class Meditation(models.Model):
    title = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='meditations/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title