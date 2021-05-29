# Youtube API sync

Frameworks used
- DRF
- Celery

Mandatory settings before running project
- Stop any containers holding port 8000, 15672, 5672
- Place Youtube API developer keys ins file YT_API/settings.py (YT_API_KEYS). You can place multiple keys in list.

To run the project 
```sh
docker-compose build
docker-compose up
```

Endpoints
Videos in desc order of published time
```sh
http://127.0.0.1:8000/videos/
```

Individual video by video_id
```sh
http://127.0.0.1:8000/videos/lBx4pbdSY_s/
```

Search videos; Replace episode with search string
```sh
http://127.0.0.1:8000/search/?q=episode
```



Files of signifance
```sh
base/models 
// Containes the Video and THumbnail model for storing videos

search/tasks.py
// Holds the poller task functions to fetch videos every 1 min

search/views.py
// Containes the views for API
```

