from .models import VideoDataModel , ThumbnailModel
from rest_framework import serializers
class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbnailModel
        exclude = ['video']

class VideoDataSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True , read_only=True)
    
    class Meta:
        model = VideoDataModel
        fields = ['video_id' , 'title' , 'description' , 'published' , 'channel_name' , 'thumbnails']
