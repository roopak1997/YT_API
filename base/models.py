from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=200)
    title = models.TextField()
    description = models.TextField()
    published_time = models.DateTimeField(db_index=True)


class Thumbnail(models.Model):
    video_ref = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='thumbnails')
    video_id = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    url = models.CharField(max_length=4000)
    width = models.IntegerField()
    height = models.IntegerField()
