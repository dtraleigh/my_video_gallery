from django import forms
from django.forms import ModelForm
from video.models import video, album, vr_shot, external_video


class new_video_form(ModelForm):
    album = forms.ModelMultipleChoiceField(queryset=album.objects.all(), widget=forms.SelectMultiple())

    class Meta:
        model = video
        fields = ["name",
                  "date_shot",
                  "poster",
                  "video_file",
                  "description",
                  "tags",
                  "lat",
                  "lon"]
        widgets = {
            "date_shot": forms.DateInput(attrs={"class": "datepicker",
                                                "id": "video_date_field"}),
            "tags": forms.SelectMultiple(),
        }


class new_vr_form(ModelForm):
    album = forms.ModelMultipleChoiceField(queryset=album.objects.all(), widget=forms.SelectMultiple())

    class Meta:
        model = vr_shot
        fields = ["name",
                  "date_shot",
                  "vr_file",
                  "poster",
                  "description",
                  "tags",
                  "lat",
                  "lon"
                  ]
        widgets = {
            "date_shot": forms.DateInput(attrs={"class": "datepicker",
                                                "id": "vr_date_field"}),
            "tags": forms.SelectMultiple(),
            "lat": forms.NumberInput(attrs={"id": "id_lat_vr"}),
            "lon": forms.NumberInput(attrs={"id": "id_lon_vr"})
        }


class edit_video_form(ModelForm):

    class Meta:
        model = video
        fields = ["name",
                  "date_shot",
                  "poster",
                  "video_file",
                  "description",
                  "tags",
                  "lat",
                  "lon"]
        widgets = {
            "date_shot": forms.DateInput(attrs={"class": "datepicker",
                                                "id": "video_date_field"}),
            "tags": forms.SelectMultiple(),
        }


class edit_vr_form(ModelForm):

    class Meta:
        model = vr_shot
        fields = ["name",
                  "date_shot",
                  "vr_file",
                  "poster",
                  "description",
                  "tags",
                  "lat",
                  "lon"
                  ]
        widgets = {
            "date_shot": forms.DateInput(attrs={"class": "datepicker",
                                                "id": "vr_date_field"}),
            "tags": forms.SelectMultiple(),
            "lat": forms.NumberInput(attrs={"id": "id_lat_vr"}),
            "lon": forms.NumberInput(attrs={"id": "id_lon_vr"})
        }
        
        
class edit_external_form(ModelForm):

    class Meta:
        model = external_video
        fields = ["name",
                  "date_shot",
                  "embed_code",
                  "poster",
                  "description",
                  "tags",
                  "lat",
                  "lon"
                  ]
        widgets = {
            "date_shot": forms.DateInput(attrs={"class": "datepicker",
                                                "id": "external_date_field"}),
            "tags": forms.SelectMultiple(),
            "lat": forms.NumberInput(attrs={"id": "id_lat_external"}),
            "lon": forms.NumberInput(attrs={"id": "id_lon_external"})
        }
