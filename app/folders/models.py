from django.db import models
from django.contrib.auth.models import User
from feeds.models import Source


# Create your models here.
class SourcesFolder(models.Model):
    """a folder to put feed sources in"""
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, related_name='source_folders', on_delete=models.CASCADE)
    sources = models.ManyToManyField(Source, related_name='folders')

    def __str__(self):
        return str(self.name)
