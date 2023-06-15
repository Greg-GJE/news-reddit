from django.shortcuts import render

from . import constants

# Create your views here.
def index(request):
    return render(request, 'users/index.html')


def login_user(request):
    if request.method == constants.POST:
        pass
    elif request.method == constants.GET:
        return render(request, 'users/login.html')
    return None


def register_user(request):
    if request.method == constants.POST:
        pass
    elif request.method == constants.GET:
        return render(request, 'users/register.html')
    return None
