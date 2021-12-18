from rest_framework.pagination import CursorPagination


class VideoDataCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-published'