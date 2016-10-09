from django.forms import ModelForm
from video.models import video

class new_video_form(ModelForm):
    class Meta:
        model = video
        fields = ['name',
                 'video_date',
                 'poster',
                 'video_file',
                 'description',
                 'tags',
                 'lat',
                 'lon']
