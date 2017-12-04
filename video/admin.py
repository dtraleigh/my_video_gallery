from django.contrib import admin
from video.models import video, album, tag, vr_shot

class video_admin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'video_date', 'poster', 'video_file')

class vr_shot_admin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'date', 'vr_file')

class album_admin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'poster', 'description')

class tag_admin(admin.ModelAdmin):
    list_display = ('name', 'date_added')

admin.site.register(video, video_admin)
admin.site.register(vr_shot, vr_shot_admin)
admin.site.register(album, album_admin)
admin.site.register(tag, tag_admin)
