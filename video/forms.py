from django import forms
from django.forms import ModelForm
from video.models import video, album, vr_shot


class new_video_form(ModelForm):
    album = forms.ModelMultipleChoiceField(queryset=album.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = video
        fields = ['name',
                 'date_shot',
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


class new_vr_form(ModelForm):
    album = forms.ModelMultipleChoiceField(queryset=album.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = vr_shot
        fields = ['name',
                  'date_shot',
                  'vr_file',
                  'description',
                  'tags',
                  'lat',
                  'lon'
                  ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'tags': forms.CheckboxSelectMultiple(),
        }