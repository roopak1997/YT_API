from rest_framework.views import APIView
from base.models import Video
from search.serializer import VideoSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import viewsets
from django.db.models import Q
import time


class VideosListSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all().order_by('-published_time')
    serializer_class = VideoSerializer


class VideoDetail(APIView):
    def get_object(self, video_id):
        try:
            return Video.objects.get(video_id=video_id)
        except Video.DoesNotExist:
            raise Http404

    def get(self, request, video_id, format=None):
        video = self.get_object(video_id)
        serializer = VideoSerializer(video)
        return Response(serializer.data)


class VideosSearchSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = VideoSerializer

    def get_queryset(self):
        search_string = self.request.GET.get("q","")
        queryset = Video.objects.filter(
            Q(title__contains=search_string) | Q(description__contains=search_string)
        )
        ordered_queryset = queryset.order_by('-published_time')
        print("search string",search_string,"filtered", ordered_queryset.count())

        return ordered_queryset


