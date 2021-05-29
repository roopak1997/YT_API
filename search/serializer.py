from rest_framework import serializers
from base.models import Video,Thumbnail


class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = ['type', 'url', 'width', 'height']


class VideoSerializer(serializers.ModelSerializer):

    thumbnails = ThumbnailSerializer(many=True)

    class Meta:
        model = Video
        fields = ['video_id', 'title', 'description', 'published_time', 'thumbnails']
