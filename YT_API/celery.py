import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YT_API.settings')

app = Celery('YT_API', include=['search.tasks'])
app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)


app.conf.beat_schedule = {
    'add-videos-every-10-min': {
        'task': 'search.tasks.get_results',
        'schedule': crontab(minute='*/1'),#30.0,
        'enabled': True
    },
}
app.conf.timezone = 'UTC'


