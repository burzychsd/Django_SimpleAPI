from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=100, null=False)
    artist = models.CharField(max_length=100, null=False)

    def __str__(self):
        return '{} - {}'.format(self.title, self.artist)