from django import forms
from video.models import video, album, tag

class new_video_form(forms.Form):
    name = forms.CharField(max_length=200)
    video_date = forms.DateField()
    poster = forms.FileField()
    video_file = forms.FileField()
    description = forms.CharField(widget=forms.Textarea)
    tags = forms.ModelMultipleChoiceField(queryset=tag.objects.all())
    lat = forms.DecimalField()
    lon = forms.DecimalField()
    album = forms.ModelMultipleChoiceField(queryset=album.objects.all())

    # class Meta:
    #     model = video
    #     fields = ['name',
    #              'video_date',
    #              'poster',
    #              'video_file',
    #              'description',
    #              'tags',
    #              'lat',
    #              'lon']
    #     widgets = {
    #         'video_date': forms.DateInput(attrs={'class':'datepicker'}),
    #     }
