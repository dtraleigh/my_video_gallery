from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from video.models import album, video, tag

def video_login(request):
    #///
    #This is the login page. The site is supposed to be password protected.
    #\\\
    message = 'Please log in'

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                message = 'Login successful.'

                return HttpResponseRedirect('/main/')
            else:
                message = 'Account is disabled.'
        else:
            message = 'Invalid login.'

    return render(request, 'login.html', {'message':message})

def video_logout(request):
    logout(request)

    return HttpResponseRedirect('/')

@login_required(login_url='/')
def main(request):
    albums = album.objects.all()

    return render(request, 'index.html', {'albums':albums})

@login_required(login_url='/')
def album_view(request, album_id):
    video_album = album.objects.get(id=album_id)
    album_videos = [v for v in video_album.videos.all()]

    return render(request, 'album.html', {'album':video_album, 'album_videos':album_videos})

@login_required(login_url='/')
def video_view(request, album_id, video_id):
    this_video = video.objects.get(id=video_id)
    video_album = album.objects.get(id=album_id)
    album_videos = [v for v in video_album.videos.all()]
    video_tags = [t for t in this_video.tags.all()]

    return render(request, 'video.html', {'video':this_video,
                                        'album':video_album,
                                        'album_videos':album_videos,
                                        'video_tags':video_tags})

@login_required(login_url='/')
def tag_view(request, tag_name):
    videos_w_tag = video.objects.filter(tags__name=tag_name)
    the_tag = tag.objects.get(name=tag_name)

    return render(request, 'tag.html', {'videos_w_tag':videos_w_tag, 'the_tag':the_tag})
