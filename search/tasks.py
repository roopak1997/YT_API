from celery import shared_task
from googleapiclient.discovery import build

import dateutil.parser
import os
import time
from celery.utils.log import get_task_logger
from django.conf import settings
import datetime
from django_celery_beat.models import PeriodicTask, PeriodicTasks

logger = get_task_logger(__name__)


def load_results(results):
    from base.models import Thumbnail, Video
    print("adding videos", len(results["items"]))

    for v in results["items"]:
        try:
            video = Video(video_id=v["id"]["videoId"],
                          title=v["snippet"]["title"],
                          description=v["snippet"]["description"],
                          published_time=dateutil.parser.parse(v["snippet"]["publishedAt"])
                          )

            video.save()

            for type in v["snippet"]["thumbnails"]:
                t = v["snippet"]["thumbnails"][type]
                thumbnail = Thumbnail(video_ref=video,
                                      video_id=v["id"]["videoId"],
                                      type=type,
                                      url=t["url"],
                                      width=t["width"],
                                      height=t["height"])
                thumbnail.save()
        except Exception as e:
            logger.info("Could not add video")
            logger.info(str(v))

@shared_task
def get_results(key_id=0):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    key = settings.YT_API_KEYS[key_id]

    youtube = build(api_service_name, api_version,
                    developerKey=key, cache_discovery=False)

    # For a 30 second poller
    publishedAfter = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

    request = youtube.search().list(
            part="snippet",
            maxResults=1000,
            publishedAfter=publishedAfter,
            q="football"
        )

    try:
        results = request.execute()
        load_results(results)

        while 'nextPageToken' in results.keys() :
            request = youtube.search().list(
                part="snippet",
                maxResults=1000,
                nextPageToken=results["nextPageToken"],
            )
            results=request.execute()
            load_results(results)

    except Exception as e:
        logger.info("Exception in YT poller ")
        logger.info(str(e))
        if 'quotaExceeded' in str(e) :
            logger.info("Quota Exceeded on %s "%settings.YT_API_KEYS[key_id])
            if key_id < len(settings.YT_API_KEYS) - 1:
                get_results(key_id + 1)
            else:
                logger.info('All keys exhausted')
                #PeriodicTask.objects.filter(task='search.tasks.get_results').update(enabled=False)
                task = PeriodicTask.objects.get(task='search.tasks.get_results')
                if task:
                    task.enabled = False
                    task.save()
                    PeriodicTasks.update_changed()



