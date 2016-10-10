from django import forms
from django.forms import ModelForm
from video.models import video, album, tag

class new_video_form(ModelForm):
    album = forms.ModelMultipleChoiceField(queryset=album.objects.all(), widget=forms.CheckboxSelectMultiple())

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
        widgets = {
            'video_date': forms.DateInput(attrs={'class':'datepicker'}),
            'tags':forms.CheckboxSelectMultiple(),
        }
