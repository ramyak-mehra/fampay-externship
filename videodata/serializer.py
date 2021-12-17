from .models import VideoDataModel
from rest_framework import serializers

class VideoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoDataModel
        fields = '__all__'