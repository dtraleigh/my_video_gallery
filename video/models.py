from django.db import models

from video.validators import validate_poster_extension, validate_video_extension


class video(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date added')
    name = models.CharField(max_length=200)
    video_date = models.DateField(verbose_name='Date taken')
    poster = models.FileField(upload_to='poster/%Y/%m/', validators=[validate_poster_extension])
    video_file = models.FileField(upload_to='video/%Y/%m/', validators=[validate_video_extension])
    description = models.TextField(default=None, blank=True, null=True)
    tags = models.ManyToManyField('tag', default=None, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    # Videos are ordered in descending order by the date they were taken. (newest to oldest)
    class Meta:
        ordering = ['-video_date']

    def __str__(self):
        return '%s, taken on %s' % (self.name, self.video_date)


class vr_video(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date added')
    name = models.CharField(max_length=200)
    date = models.DateField(verbose_name='Date shot')
    video_file = models.FileField(upload_to='vr/%Y/%m/')
    description = models.TextField(default=None, blank=True, null=True)
    tags = models.ManyToManyField('tag', default=None, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    # VR shots are ordered in descending order by the date they were taken. (newest to oldest)
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return '%s, taken on %s' % (self.name, self.date)


class album(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date added')
    name = models.CharField(max_length=200, unique=True)
    videos = models.ManyToManyField('video', default=None, blank=True)
    description = models.TextField(default=None, blank=True, null=True)
    poster = models.FileField(upload_to='poster/%Y/%m/')

    def __str__(self):
        return '%s' % (self.name)


class tag(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date added')
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return '%s' % (self.name)
