from django.apps import AppConfig
import os
from decouple import config
import schedule
class VideodataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videodata'

    def ready(self):
        # Django runs the program multiple times, so we need to make sure
        # that the job is created only once.
        if os.environ.get('RUN_MAIN' , None) != 'true':
            from .data_fetch import YoutubeAPIClient
            from .jobs import ScheduleJob
            client = YoutubeAPIClient(
                query='Google',max_results=10,
                pageToken=config('NEXT_PAGE_TOKEN', default=None),
                maxTries=config('MAX_TRIES', default=1, cast=int)
            )
            scheduleJob = ScheduleJob(client)
            client.scheduleJob = scheduleJob
            scheduleJob.start_scheduler(10)
