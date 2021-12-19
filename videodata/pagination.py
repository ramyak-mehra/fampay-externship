from rest_framework.pagination import CursorPagination

"""
Custom cursor based pagination to change the ordering field.
"""
class VideoDataCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-published'