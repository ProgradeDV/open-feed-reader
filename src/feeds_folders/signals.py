"""Signals for folder initialization."""
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from .models import FeedsFolder


@receiver(post_save, sender=User)
def create_favorites_folder(sender:Signal, instance:User, created:bool, **kwargs:any) -> None:  # noqa: ARG001
    """Signal to create a "Favorites" forlder for each new user."""
    if created:
        FeedsFolder.objects.create(name="★ Favorites", user=instance)
