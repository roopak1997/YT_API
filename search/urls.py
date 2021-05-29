from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from search import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'videos', views.VideoList)

videos_list = views.VideosListSet.as_view({
    'get' : 'list'
})

search_list = views.VideosSearchSet.as_view({
    'get' : 'list'
})

urlpatterns = [
    path('videos/', videos_list, name='videos-list'),
    path('videos/<str:video_id>/', views.VideoDetail.as_view()),
    path('search/', search_list, name='search-list')
]


urlpatterns = format_suffix_patterns(urlpatterns)
