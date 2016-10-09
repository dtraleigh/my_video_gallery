from django.conf.urls import url
from django.contrib import admin
from video import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.video_login),
    url(r'^main/$', views.main),
    url(r'^main/upload/$', views.upload),
    url(r'^logout/$', views.video_logout),
    url(r'^album/(?P<album_id>[0-9]+)$', views.album_view),
    url(r'^album/(?P<album_id>[0-9]+)/video/(?P<video_id>[0-9]+)$', views.video_view),
    url(r'^tag/(?P<tag_name>[\w|\W]+)/video/(?P<video_id>[0-9]+)$', views.video_tag_view),
    url(r'^tag/(?P<tag_name>[\w|\W]+)$', views.tag_view),
    url(r'^recent/(?P<video_id>[0-9]+)$', views.recent_view),
]
