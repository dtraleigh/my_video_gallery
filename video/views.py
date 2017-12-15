from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from video.models import album, video, tag, vr_shot
from video.forms import new_video_form, new_vr_form

from itertools import chain
from operator import attrgetter
import logging
logger = logging.getLogger('video_log')


def is_most_recent(this_shot, shot_list):
    if [i.id for i in shot_list].index(this_shot.id) == 0:
        return True
    else:
        return False


def is_oldest(this_shot, shot_list):
    if [i.id for i in shot_list].index(this_shot.id) == len(shot_list) - 1:
        return True
    else:
        return False


def get_next_shot(curr_shot, shot_list):
    # Find the position that curr_shot is in
    # next_shot is the one in the after it
    next_shot = shot_list[[i.id for i in shot_list].index(curr_shot.id) - 1]

    return next_shot


def get_prev_shot(curr_shot, shot_list):
    # Find the position that curr_video is in
    # next_video is the one in the before it
    prev_shot = shot_list[[i.id for i in shot_list].index(curr_shot.id) + 1]

    return prev_shot


def combine_and_sort(vr_list, video_list):
    shots_sorted = sorted(
        chain(vr_list, video_list),
        key=attrgetter('date_shot'))

    return shots_sorted[::-1]


def video_login(request):
    # This is the login page. The site is supposed to be password protected.
    message = 'Please log in'
    next = ""

    if request.GET:
        next = request.GET['next']

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                message = 'Login successful.'

                if next == '':
                    return HttpResponseRedirect('/main/')
                else:
                    return HttpResponseRedirect(next)
            else:
                message = 'Account is disabled.'
        else:
            message = 'Invalid login.'

    return render(request, 'login.html', {'message': message,
                                          'next': next})


def video_logout(request):
    logout(request)

    return HttpResponseRedirect('/')


@login_required(redirect_field_name='next')
def main(request):
    tag_list = tag.objects.all()
    albums = album.objects.all()

    all_videos = [v for v in video.objects.all()]
    all_vr = [vr for vr in vr_shot.objects.all()]

    all_shots = combine_and_sort(all_vr, all_videos)

    most_recent = all_shots[0:6]

    # We need the albums to be sorted by the videos within most recently added date_added
    albums_most_recent_list = []

    for an_album in albums:
        # If not empty album
        if len(an_album.videos.all()) > 0:
            albums_most_recent = an_album.videos.latest('date_added')

            albums_most_recent_list.append([str(albums_most_recent.date_added), an_album])

    # Sort by date_added in descending order
    albums_sorted_w_date = sorted(albums_most_recent_list, key=lambda x: x[0], reverse=True)

    # Get a list of just the albums now that they are sorted by date_added
    sorted_albums = []

    for a in albums_sorted_w_date:
        sorted_albums.append(a[1])

    return render(request, 'index.html', {'albums': sorted_albums,
                                          'tag_list': tag_list,
                                          'most_recent': most_recent})


@login_required(redirect_field_name='next')
def upload(request):
    if request.method == 'POST':
        upload_form = new_video_form(request.POST, request.FILES)
        upload_vr_form = new_vr_form(request.POST, request.FILES)

        if upload_form.is_valid():
            new_video = upload_form.save()

            album_choice = upload_form.cleaned_data['album']
            # logger.debug(album_choice)
            for a in album_choice:
                a.videos.add(new_video)
                a.save()

            messages.info(request, 'Successfully uploaded ' + new_video.name + '.')

            if 'save_video' in request.POST:
                return HttpResponseRedirect('/main/upload/')
            if 'save_video_and_main' in request.POST:
                return HttpResponseRedirect('/main/')

        if upload_vr_form.is_valid():
            new_vr_shot = upload_vr_form.save()

            album_choice = upload_vr_form.cleaned_data['album']
            for a in album_choice:
                a.vr_shots.add(new_vr_shot)
                a.save()

            messages.info(request, 'Successfully uploaded ' + new_vr_shot.name + '.')

            if 'save_vr' in request.POST:
                return HttpResponseRedirect('/main/upload/')
            if 'save_vr_and_main' in request.POST:
                return HttpResponseRedirect('/main/')

    else:
        upload_form = new_video_form()
        upload_vr_form = new_vr_form()

    return render(request, 'upload.html', {'upload_form': upload_form,
                                           'upload_vr_form': upload_vr_form})


@login_required(redirect_field_name='next')
def album_view(request, album_id):
    video_and_vr_album = album.objects.get(id=album_id)

    album_videos = [v for v in video_and_vr_album.videos.all()]
    album_vrs = [vr for vr in video_and_vr_album.vr_shots.all()]

    content = combine_and_sort(album_vrs, album_videos)

    return render(request, 'album.html', {'album': video_and_vr_album,
                                          'album_videos': content})


@login_required(redirect_field_name='next')
def shot_view(request, album_id, shot_type, shot_id):
    # The shot the user wants to see
    if shot_type == "video":
        this_shot = video.objects.get(id=shot_id)
    elif shot_type == "vr":
        this_shot = vr_shot.objects.get(id=shot_id)

    # The album the user is within
    video_and_vr_album = album.objects.get(id=album_id)

    album_videos = [v for v in video_and_vr_album.videos.all()]
    album_vrs = [vr for vr in video_and_vr_album.vr_shots.all()]

    # All the shots within this album
    album_shots = combine_and_sort(album_vrs, album_videos)

    shot_tags = [t for t in this_shot.tags.all()]

    if not is_most_recent(this_shot, album_shots):
        next_video = get_next_shot(this_shot, album_shots)
        no_next = False
    else:
        next_video = this_shot
        no_next = True

    if not is_oldest(this_shot, album_shots):
        prev_video = get_prev_shot(this_shot, album_shots)
        no_prev = False
    else:
        prev_video = this_shot
        no_prev = True

    album_view = True

    return render(request, 'shot.html', {'video': this_shot,
                                         'album': video_and_vr_album,
                                         'album_videos': album_shots,
                                         'video_tags': shot_tags,
                                         'album_view': album_view,
                                         'next_video': next_video,
                                         'no_next': no_next,
                                         'no_prev': no_prev,
                                         'prev_video': prev_video})


@login_required(redirect_field_name='next')
def tag_view(request, tag_name):
    videos_w_tag = video.objects.filter(tags__name=tag_name)
    vr_w_tag = vr_shot.objects.filter(tags__name=tag_name)

    # All the shots with this tag
    videos_w_tag = combine_and_sort(videos_w_tag, vr_w_tag)

    the_tag = tag.objects.get(name=tag_name)

    return render(request, 'tag.html', {'videos_w_tag': videos_w_tag,
                                        'the_tag': the_tag})


@login_required(redirect_field_name='next')
def video_tag_view(request, tag_name, shot_type, shot_id):
    # The shot the user wants to see
    if shot_type == "video":
        this_shot = video.objects.get(id=shot_id)
    elif shot_type == "vr":
        this_shot = vr_shot.objects.get(id=shot_id)

    # The tag the user clicked on
    the_tag = tag.objects.get(name=tag_name)

    # This shot's tags
    shot_tags = [t for t in this_shot.tags.all()]

    # All shots that have this tag
    shots_w_tag = video.objects.filter(tags__name=tag_name)

    if not is_most_recent(this_shot, shots_w_tag):
        next_video = get_next_shot(this_shot, shots_w_tag)
        no_next = False
    else:
        next_video = this_shot
        no_next = True

    if not is_oldest(this_shot, shots_w_tag):
        prev_video = get_prev_shot(this_shot, shots_w_tag)
        no_prev = False
    else:
        prev_video = this_shot
        no_prev = True

    tag_view = True

    return render(request, 'shot.html', {'video': this_shot,
                                         'the_tag': the_tag,
                                         'video_tags': shot_tags,
                                         'tag_view': tag_view,
                                         'next_video': next_video,
                                         'no_next': no_next,
                                         'no_prev': no_prev,
                                         'prev_video': prev_video})


@login_required(redirect_field_name='next')
def recent_view(request, shot_type, shot_id):
    # The shot the user wants to see
    if shot_type == "video":
        this_shot = video.objects.get(id=shot_id)
    elif shot_type == "vr":
        this_shot = vr_shot.objects.get(id=shot_id)

    all_videos = video.objects.all()
    all_vr = vr_shot.objects.all()

    all_shots = combine_and_sort(all_vr, all_videos)

    video_tags = [t for t in this_shot.tags.all()]

    if not is_most_recent(this_shot, all_shots):
        next_video = get_next_shot(this_shot, all_shots)
        no_next = False
    else:
        next_video = this_shot
        no_next = True

    if not is_oldest(this_shot, all_shots):
        prev_video = get_prev_shot(this_shot, all_shots)
        no_prev = False
    else:
        prev_video = this_shot
        no_prev = True

    recent_view = True

    return render(request, 'shot.html', {'video': this_shot,
                                         'video_tags': video_tags,
                                         'next_video': next_video,
                                         'prev_video': prev_video,
                                         'no_next': no_next,
                                         'no_prev': no_prev,
                                         'recent_view': recent_view})
