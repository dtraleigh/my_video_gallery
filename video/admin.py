from django.contrib import admin
from video.models import video, album, tag

class video_admin(admin.ModelAdmin):
    list_display = ('date_added', 'name', 'video_date', 'poster', 'video_file', 'description')

class album_admin(admin.ModelAdmin):
    list_display = ('date_added', 'name', 'poster', 'description')

class tag_admin(admin.ModelAdmin):
    list_display = ('date_added', 'name')

admin.site.register(video, video_admin)
admin.site.register(album, album_admin)
admin.site.register(tag, tag_admin)
