from django.db import models

# Create your models here.
class VideoDataModel(models.Model):
    video_id = models.CharField(max_length=100)
    # youtube video title max length is 120. 20 more just in case it chanegs.
    title = models.CharField(max_length=100)
    description = models.TextField()
    published = models.DateTimeField()
    # youtube channel name max length is 60. 100 just in case the it changes.
    channel_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.title}_{self.video_id}"
class ThumbnailModel(models.Model):
    video = models.ForeignKey(VideoDataModel, related_name='thumbnails', on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    image = models.ImageField(upload_to='thumbnails')
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.title}_{self.video_id}"