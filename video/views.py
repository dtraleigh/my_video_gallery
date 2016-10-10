from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from video.models import album, video, tag
from video.forms import new_video_form

def is_most_recent(this_video, video_list):
    if [i.id for i in video_list].index(this_video.id) == 0:
        return True
    else:
        return False

def is_oldest(this_video, video_list):
    if [i.id for i in video_list].index(this_video.id) == len(video_list) - 1:
        return True
    else:
        return False

def get_next_video(curr_video, video_list):
    #Find the position that curr_video is in
    #next_video is the one in the before after it
    next_video = video_list[[i.id for i in video_list].index(curr_video.id) - 1]

    return next_video

def get_prev_video(curr_video, video_list):
    #Find the position that curr_video is in
    #next_video is the one in the before after it
    prev_video = video_list[[i.id for i in video_list].index(curr_video.id) + 1]

    return prev_video

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
    tag_list = tag.objects.all()
    albums = album.objects.all()
    most_recent = video.objects.all()[0:6]

    #Go through each album and find the most recent video taken.
    albums_and_most_recent_date = []

    for an_album in albums:
        album_videos = [v for v in an_album.videos.all()]
        if len(album_videos) > 0:
            most_recent_video = album_videos[0]
            for a_video in album_videos:
                if a_video.video_date > most_recent_video.video_date:
                    most_recent_video = a_video

        albums_and_most_recent_date.append([an_album, str(most_recent_video.video_date)])

    albums_sorted_w_date = sorted(albums_and_most_recent_date, key=lambda d: d[1], reverse=True)

    sorted_albums = []

    for an_album in albums_sorted_w_date:
        sorted_albums.append(an_album[0])

    return render(request, 'index.html', {'albums':sorted_albums,
                                        'tag_list':tag_list,
                                        'most_recent':most_recent})

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required(login_url='/')
def upload(request):
    if request.method == 'POST':
        upload_form = new_video_form(request.POST, request.FILES)

        if upload_form.is_valid():
            upload_form.save()
            # name = upload_form.cleaned_data['name']
            # video_date = upload_form.cleaned_data['video_date']
            # description = upload_form.cleaned_data['description']
            # lat = upload_form.cleaned_data['lat']
            # lon = upload_form.cleaned_data['lon']
            #
            # handle_uploaded_file(request.FILES['poster'])
            # handle_uploaded_file(request.FILES['video_file'])



            return HttpResponseRedirect('/main/upload/')

    else:
        upload_form = new_video_form()

    return render(request, 'upload.html', {'upload_form':upload_form})

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

    if not is_most_recent(this_video, album_videos):
        next_video = get_next_video(this_video, album_videos)
        no_next = False
    else:
        next_video = this_video
        no_next = True

    if not is_oldest(this_video, album_videos):
        prev_video = get_prev_video(this_video, album_videos)
        no_prev = False
    else:
        prev_video = this_video
        no_prev = True

    album_view = True

    return render(request, 'video.html', {'video':this_video,
                                        'album':video_album,
                                        'album_videos':album_videos,
                                        'video_tags':video_tags,
                                        'album_view':album_view,
                                        'next_video':next_video,
                                        'no_next':no_next,
                                        'no_prev':no_prev,
                                        'prev_video':prev_video})

@login_required(login_url='/')
def tag_view(request, tag_name):
    videos_w_tag = video.objects.filter(tags__name=tag_name)
    the_tag = tag.objects.get(name=tag_name)

    return render(request, 'tag.html', {'videos_w_tag':videos_w_tag, 'the_tag':the_tag})

@login_required(login_url='/')
def video_tag_view(request, tag_name, video_id):
    this_video = video.objects.get(id=video_id)
    the_tag = tag.objects.get(name=tag_name)
    video_tags = [t for t in this_video.tags.all()]
    videos_w_tag = video.objects.filter(tags__name=tag_name)

    if not is_most_recent(this_video, videos_w_tag):
        next_video = get_next_video(this_video, videos_w_tag)
        no_next = False
    else:
        next_video = this_video
        no_next = True

    if not is_oldest(this_video, videos_w_tag):
        prev_video = get_prev_video(this_video, videos_w_tag)
        no_prev = False
    else:
        prev_video = this_video
        no_prev = True

    tag_view = True

    return render(request, 'video.html', {'video':this_video,
                                        'the_tag':the_tag,
                                        'video_tags':video_tags,
                                        'tag_view':tag_view,
                                        'next_video':next_video,
                                        'no_next':no_next,
                                        'no_prev':no_prev,
                                        'prev_video':prev_video})

@login_required(login_url='/')
def recent_view(request, video_id):
    this_video = video.objects.get(id=video_id)
    all_videos = video.objects.all()
    video_tags = [t for t in this_video.tags.all()]

    if not is_most_recent(this_video, all_videos):
        next_video = get_next_video(this_video, all_videos)
        no_next = False
    else:
        next_video = this_video
        no_next = True

    if not is_oldest(this_video, all_videos):
        prev_video = get_prev_video(this_video, all_videos)
        no_prev = False
    else:
        prev_video = this_video
        no_prev = True

    recent_view = True

    return render(request, 'video.html', {'video':this_video,
                                        'video_tags':video_tags,
                                        'next_video':next_video,
                                        'prev_video':prev_video,
                                        'no_next':no_next,
                                        'no_prev':no_prev,
                                        'recent_view':recent_view})
