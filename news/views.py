from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from newsapi import NewsApiClient
import json
import requests

from bs4 import BeautifulSoup

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.template.defaultfilters import slugify

from django.contrib.auth.decorators import login_required

from .models import FeaturedNews, Timestamp


def fetch_country_code():
    # getting the geolocation response
    geolocation_response = requests.get(
        settings.GEOLOCATION_API_URL, verify=False, timeout=10)

    if geolocation_response is not None and geolocation_response.content is not None:
        data = json.loads(geolocation_response.content)
        return data.get('country_code')

    return None


def add_to_database_from_api(news_api_client, category, country_code):
    news_api_client = NewsApiClient(api_key=settings.NEWSAPI_KEY)

    if category == 'headlines':

        top_news_response = news_api_client.get_top_headlines(
            language='en', country=country_code.lower())
    else:
        top_news_response = news_api_client.get_top_headlines(
            language='en', category=category, country=country_code.lower()
        )
    # max news
    MAX_NEWS_EACH_CATEGORY = 6

    # first of all getting the top_news_response
    if top_news_response is not None and top_news_response.get('articles') is not None:
        current_total = 0
        for top_news in top_news_response.get('articles'):
            if current_total >= MAX_NEWS_EACH_CATEGORY:
                break
            if top_news.get('title') is not None and \
                    top_news.get('description') is not None and \
                    top_news.get('content') is not None:
                if not FeaturedNews.objects.filter(slug=slugify(top_news.get('title'))):
                    current_news = FeaturedNews(title=top_news.get('title'),
                                                author=top_news.get(
                                                    'author', 'anonymous'),
                                                description=top_news.get(
                        'description'),
                        content=top_news.get(
                        'content'),
                        category=category,
                        url=top_news.get('url'),
                        image_url=top_news.get(
                        'urlToImage'),
                        published_date=parse_datetime(
                        top_news.get('publishedAt'))
                    )
                    current_news.save()
                    current_total += 1
                else:
                    continue


# Create your views here.
def populate_featured_news_database():
    # check the timestamp table first
    # if there is no timestamp or the current timestamp value is 1 hour before
    # then do the db populating
    will_populate_db = False
    if not Timestamp.objects.all().exists():
        current_timestamp = Timestamp()
        current_timestamp.save()
        will_populate_db = True

    present_timestamp = timezone.now()
    current_timestamp_object = Timestamp.objects.all()[0]
    stored_timestamp = current_timestamp_object.creationDate

    elapsed_time_in_hours = (
        present_timestamp - stored_timestamp).seconds / 3600

    if elapsed_time_in_hours >= 5:
        # more than an hour has passed so we need to add updated news to the collection
        will_populate_db = True

        # update the timestamp
        current_timestamp_object.creationDate = present_timestamp
        current_timestamp_object.save()

    if will_populate_db:
        # populate the db
        country_code = fetch_country_code()

        if country_code is None:
            country_code = 'us'

        news_api_client = NewsApiClient(api_key=settings.NEWSAPI_KEY)

        # first of all delete all the records from the table
        FeaturedNews.objects.all().delete()

        add_to_database_from_api(news_api_client, "headlines", country_code)
        add_to_database_from_api(news_api_client, "business", country_code)
        add_to_database_from_api(news_api_client, "technology", country_code)
        add_to_database_from_api(news_api_client, "sports", country_code)


def index(request):

    populate_featured_news_database()

    featured_news = FeaturedNews.objects.filter(
        category="headlines").order_by("-published_date")[:6]
    business_news = FeaturedNews.objects.filter(
        category="business").order_by("-published_date")[:6]
    tech_news = FeaturedNews.objects.filter(
        category="technology").order_by("-published_date")[:6]
    sports_news = FeaturedNews.objects.filter(
        category="sports").order_by("-published_date")[:6]

    context = {
        'featured': featured_news,
        'business': business_news,
        'technology': tech_news,
        'sports': sports_news
    }

    return render(request, 'news/index.html', context=context)


@login_required(login_url='/users/login')
def featured_news_detail(request, slug):
    news = get_object_or_404(FeaturedNews, slug=slug)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

    r = requests.get(news.url, headers=headers, timeout=5)
    soup = BeautifulSoup(r.content, "html.parser")

    # print(soup.prettify())

    content = []
    for paragraph in soup.find_all('p'):
        paragraph_text = paragraph.get_text()
        if len(paragraph_text) > 0:
            content.append(f'<p>{paragraph.get_text()}</p>')

    # use beautiful soup to extract the url

    if len(content) == 0:
        try:
            text = news.content[:news.content.index('[+')]
        except ValueError:
            text = news.content
    else:
        text = ''.join(content)

    context = {
        'news': news,
        'text': text
    }
    return render(request, 'news/featured_news_detail.html', context=context)


def search(request):
    # here will be calling the search api
    search_term = request.GET.get('search')
    if search_term is None or search_term.strip() == '':
        return redirect(reverse('news:index'))

    # call the news api and fetch the data

    search_results = []

    news_api_client = NewsApiClient(api_key=settings.NEWSAPI_KEY)

    articles = news_api_client.get_everything(q=search_term, sort_by='relevancy', page=1, language='en')

    if articles is not None and articles.get('articles') is not None:
        print(len(articles.get('articles')))
        for article in articles.get('articles')[:50]:
            if article.get('title') is not None and article.get('description') is not None and article.get('urlToImage') is not None:
                search_results.append({
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'author': article.get('author', 'anonymous'),
                    'image_url': article.get('urlToImage'),
                    'url': article.get('url'),
                    'published_date': article.get('publishedAt')
                })

    print(search_results)

    context = {'term': search_term, 'search_results': search_results,  'count': len(search_results)}
    return render(request, 'news/search_results.html', context=context)
