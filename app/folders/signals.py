from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import SourcesFolder

@receiver(post_save, sender=User)
def create_favorites_folder(sender, instance, created, **kwargs):
    """Signal to create a "Favorites" forlder for each new user"""
    if created:
        SourcesFolder.objects.create(name="★ Favorites", user=instance)
