from django.apps import AppConfig


class FeedSubscriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed_subscriptions'

    def ready(self):
        from . import signals
