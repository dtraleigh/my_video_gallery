from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

    return render(request, 'index.html')

@login_required(login_url='/')
def upload(request):

    return render(request, 'upload.html')
