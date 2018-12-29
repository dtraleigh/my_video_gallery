from django.contrib import admin
from video.models import *


class video_admin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'date_shot', 'poster', 'video_file', 'get_tags', 'lat', 'lon')

class vr_shot_admin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'date_shot', 'poster', 'vr_file')


class album_admin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'poster', 'description')


class tag_admin(admin.ModelAdmin):
    list_display = ('name', 'date_added')


class location_admin(admin.ModelAdmin):
    list_display = ('name', 'label', 'lat', 'lon', 'htmlid')


admin.site.register(video, video_admin)
admin.site.register(vr_shot, vr_shot_admin)
admin.site.register(album, album_admin)
admin.site.register(tag, tag_admin)
admin.site.register(location, location_admin)
