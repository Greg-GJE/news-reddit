from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Count

from news.models import CommunityNews

from . import constants


def index(request):
    return redirect(reverse('users:user_profile'))


@login_required(login_url='/users/login')
def fetch_user_details(request, username=None):

    user_model = get_user_model()

    current = False

    if username is None or username == request.user.username:
        # fetch the current profile
        user = request.user
        current = True
    else:
        user = get_object_or_404(user_model, username=username)

    news = user.news.order_by("-published_at")

    context = {'current': current, 'user': user, 'profile_news': news}
    return render(request, 'users/profile.html', context=context)


def login_user(request):
    if request.method == constants.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_model = get_user_model()

        if not user_model.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect(reverse('users:login'))

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect(reverse('users:login'))
        else:
            login(request, user)
            return redirect(request.GET.get('next', reverse('news:index')))

    elif request.method == constants.GET:
        if not request.user.is_authenticated:
            return render(request, 'users/login.html')

        return redirect(request.GET.get('next', reverse('news:index')))
    return None


def register_user(request):
    if request.method == constants.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_model = get_user_model()

        existing_user_by_username = user_model.objects.filter(
            username=username)

        if existing_user_by_username.exists():
            messages.error(request, 'Username already taken')
            return redirect(reverse('users:register'))

        # checking user by email
        existing_user_by_email = user_model.objects.filter(email=email)

        if existing_user_by_email.exists():
            messages.error(request, 'Email already exists. Try to login')
            return redirect(reverse('users:register'))

        # now try to save the user
        user = user_model.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )

        # setting the password
        user.set_password(password)

        user.save()

        messages.success(request, 'User created successfully! Login now')
        return redirect(reverse('users:login'))

    elif request.method == constants.GET:
        if not request.user.is_authenticated:
            return render(request, 'users/register.html')

        return redirect(reverse('news:index'))
    return None


@login_required(login_url="/users/login")
def delete_news(request):
    if request.method == 'POST':
        slug = request.POST.get('news_slug')
        if slug is not None and slug != '':
            news_to_delete = CommunityNews.objects.get(slug=slug)
            print(news_to_delete)

            # deleting the news
            news_to_delete.delete()

            return redirect(reverse('users:user_profile'))

    return redirect(reverse('news:community'))


def show_all_profiles(request):
    user_model = get_user_model()

    all_users = user_model.objects.alias(
        news_count=Count('news')).order_by('-news_count')

    total_users = all_users.count()

    context = {
        'users': all_users,
        'total_results': total_users
    }

    return render(request, 'users/all_users.html', context=context)


def search_profiles(request):
    if request.method == 'GET':
        if request.GET.get('search') is not None and request.GET.get('search') != '':
            search_term = request.GET.get('search')

            user_model = get_user_model()

            searched_users = user_model.objects.filter(
                username__icontains=search_term)

            found_users = searched_users.count()

            context = {
                'users': searched_users,
                'total_results': found_users,
                'term': search_term
            }

            return render(request, 'users/search_profiles.html', context=context)

    return redirect(reverse('users:all'))


def logout_user(request):
    logout(request)
    return redirect(reverse('news:index'))


@login_required(login_url='/users/login')
def upload_avatar(request):
    if request.method == 'POST' and request.user is not None:

        current_profile = request.user.profile
        current_profile.image = request.FILES.get('avatar')
        current_profile.save()

    return redirect(reverse('users:user_profile'))
