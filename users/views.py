from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from . import constants

# Create your views here.
def index(request):
    return render(request, 'users/index.html')


def login_user(request):
    if request.method == constants.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_model = get_user_model()

        if not user_model.objects.filter(username = username).exists():
            messages.error(request, 'Invalid Username')
            return redirect(reverse('users:login'))

        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect(reverse('users:login'))
        else:
            login(request, user)
            return redirect(reverse('news:index'))


    elif request.method == constants.GET:
        return render(request, 'users/login.html')
    return None


def register_user(request):
    if request.method == constants.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_model = get_user_model()

        existing_user_by_username = user_model.objects.filter(username = username)

        if existing_user_by_username.exists():
            messages.error(request, 'Username already taken')
            return redirect(reverse('users:register'))

        # checking user by email
        existing_user_by_email = user_model.objects.filter(email = email)

        if existing_user_by_email.exists():
            messages.error(request, 'Email already exists. Try to login')
            return redirect(reverse('users:register'))

        # now try to save the user


    elif request.method == constants.GET:
        return render(request, 'users/register.html')
    return None

def logout_user(request):
    logout(request)
    return redirect(reverse('news:index'))
