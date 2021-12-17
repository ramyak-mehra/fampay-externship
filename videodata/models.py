from django.db import models

# Create your models here.
class VideoDataModel(models.Model):
    video_id = models.CharField(max_length=100)
    # youtube video title max length is 100
    title = models.CharField(max_length=100)
    description = models.TextField()
    published = models.DateTimeField()