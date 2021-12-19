import schedule
from .data_fetch import YoutubeAPIClient
from schedule import Scheduler
import threading
import time

def fetch_videos(client):
    client.execute()
"""
Out of the box it is not possible to run the schedule in the background.
However, we can create a thread ourself and use it to run jobs without
blocking the main thread.
Reference :https://schedule.readthedocs.io/en/stable/background-execution.html
"""
def run_continuously(self, interval=1):
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run
# A little hack so that the Scheduler can use the custom run_continuously.
Scheduler.run_continuously = run_continuously

#Schedule Job class to manage the jobs from anywhere.
class ScheduleJob():
    def __init__(self,client):
        self.client = client
        self.scheduler = Scheduler()

    def start_scheduler(self,interval=1):
        print('Starting scheduler')
        self.job = self.scheduler.every(interval).second.do(fetch_videos , client=self.client)
        self.scheduler.run_continuously()
    
    def stop_scheduler(self):
        print('Stopping scheduler')
        self.scheduler.clear()