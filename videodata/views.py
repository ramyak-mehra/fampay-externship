from django_filters.rest_framework import filters
from .serializer import VideoDataSerializer
from .models import VideoDataModel
from .pagination import VideoDataCursorPagination
from rest_framework import pagination, viewsets
from rest_framework import filters
"""
We are using viewsets.ReadOnlyModelViewSet 
because we only need to read data from the database.

"""
class VideoDataViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset provides 'list' and 'retrive' end points for Video Data.
    """
    queryset = VideoDataModel.objects.all()
    serializer_class = VideoDataSerializer
    pagination_class  = VideoDataCursorPagination
    filter_backends = [filters.SearchFilter , filters.OrderingFilter]
    search_fields= ['title' , 'description' , 'video_id']
    ordering_fields = ['published' , 'title' , 'channel_name']
    ordering = ['-published']


