
from django.db import models
from django.conf import settings

class Meditation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='meditations/', blank=True, null=True)
    video_file = models.FileField(upload_to='meditations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title