"""
Defines the user subscriptions and compartmentalizations
"""

from django.db import models
from django.contrib.auth.models import User
from feeds.models import Source, Entry


class SourceSubcription(models.Model):
    """a users subscription to a feed source"""
    user = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    source = models.ForeignKey(Source, related_name='subscriptions', on_delete=models.CASCADE)


class SourcesFolder(models.Model):
    """a folder to put feed sources in"""
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, related_name='source_folders', on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField(SourceSubcription, related_name='folders')


class PostsFolder(models.Model):
    """a folder to put posts in"""
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, related_name='post_folders', on_delete=models.CASCADE)
    posts = models.ManyToManyField(Entry, related_name='saved_folders')
