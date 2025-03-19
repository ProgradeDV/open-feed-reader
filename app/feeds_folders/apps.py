from django.apps import AppConfig


class FeedsFoldersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feeds_folders'

    def ready(self):
        from feeds_folders import signals
