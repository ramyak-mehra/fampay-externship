from django_filters.rest_framework import filters
from .serializer import VideoDataSerializer
from .models import VideoDataModel
from .pagination import VideoDataCursorPagination
from rest_framework import pagination, viewsets
from rest_framework import filters
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

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
    """
    We cache the result for 10 minutes. As new data is only available only after 10 mins.
    We are currently using the default local memory caching. But can be easily replaced with redis
    or any other by configuring the CACHE in the settings file. No changes are required here.
    """
    @method_decorator(cache_page(60*10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60*10))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
