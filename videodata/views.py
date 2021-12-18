from .serializer import VideoDataSerializer
from .models import VideoDataModel
from .pagination import VideoDataCursorPagination
from rest_framework import pagination, viewsets

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

