from django.apps import AppConfig

class VideodataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videodata'

    def ready(self):
        from .data_fetch import YoutubeAPIClient
        client = YoutubeAPIClient(
            query='Google',max_results=10
        )
        client.execute()
        return super().ready()