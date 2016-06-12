from django.db import models

class video(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date added')
    name = models.CharField(max_length=200)
    video_date = models.DateField(verbose_name='Date taken')
    poster = models.FileField(upload_to='poster/%Y/%m/')
    video_file = models.FileField(upload_to='video/%Y/%m/')
    description = models.TextField(default=None, blank=True, null=True)
    tags = models.ManyToManyField('tag', default=None, blank=True)

    def __str__(self):
        return '%s' % (self.name)

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
