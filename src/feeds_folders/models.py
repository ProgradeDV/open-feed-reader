"""Models for feed folders."""
from django.contrib.auth.models import User
from django.db import models

from feeds.models import Source


# Create your models here.
class FeedsFolder(models.Model):
    """Folder to put feed sources in."""

    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, related_name="source_folders", on_delete=models.CASCADE)
    feeds = models.ManyToManyField(Source, related_name="folders")

    def __str__(self) -> str:
        """Use the name attribute for string."""
        return str(self.name)
