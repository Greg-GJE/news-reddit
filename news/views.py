from django.shortcuts import render
from django.conf import settings
from newsapi import NewsApiClient
import json
import requests

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.template.defaultfilters import slugify

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
            language='en', category=category
        )
    # max news
    MAX_NEWS_EACH_CATEGORY = 6

    # first of all getting the top_news_response
    if top_news_response is not None and top_news_response.get('articles') is not None:
        current_total = 0
        for top_news in top_news_response.get('articles'):
            if current_total >= MAX_NEWS_EACH_CATEGORY:
                break
            if top_news.get('title') is not None and top_news.get('description') is not None and top_news.get('content') is not None:
                if not FeaturedNews.objects.filter(slug=slugify(top_news.get('title'))).exists():
                    current_news = FeaturedNews(title=top_news.get('title'),
                                                author=top_news.get('author', 'anonymous'),
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
    stored_timestamp = Timestamp.objects.all()[0].creationDate

    elapsed_time_in_hours = (
        present_timestamp - stored_timestamp).seconds / 3600

    if elapsed_time_in_hours >= 1:
        # more than an hour has passed so we need to add updated news to the collection
        will_populate_db = True

    if will_populate_db:
        # populate the db
        country_code = fetch_country_code()

        if country_code is None:
            country_code = 'us'

        news_api_client = NewsApiClient(api_key=settings.NEWSAPI_KEY)

        add_to_database_from_api(news_api_client, "headlines", country_code)
        add_to_database_from_api(news_api_client, "business", country_code)
        add_to_database_from_api(news_api_client, "technology", country_code)
        add_to_database_from_api(news_api_client, "sports", country_code)


def index(request):


    populate_featured_news_database()



    featured_news = FeaturedNews.objects.filter(category="headlines").order_by("-published_date")
    business_news = FeaturedNews.objects.filter(category="business").order_by("-published_date")
    tech_news = FeaturedNews.objects.filter(category="technology").order_by("-published_date")
    sports_news = FeaturedNews.objects.filter(category="sports").order_by("-published_date")

    # if top_news_response is not None:
    #     featured_news_list = top_news_response['articles'][:6]
    #     for news in featured_news_list:
    #         featured_news.append({
    #             'author': 'anonymous' if news['author'] is None else news['author'],
    #             'title': news['title'],
    #             'description': news['description'],
    #             'url': news['url'],
    #             'imageUrl': news['urlToImage'],
    #             'publishedAt': news['publishedAt']
    #         })

    # if top_business_news_response is not None:
    #     business_news_list = top_business_news_response['articles'][1:7]
    #     for news in business_news_list:
    #         business_news.append({
    #             'author': 'anonymous' if news['author'] is None else news['author'],
    #             'title': news['title'],
    #             'description': news['description'],
    #             'url': news['url'],
    #             'imageUrl': news['urlToImage'],
    #             'publishedAt': news['publishedAt']
    #         })

    # if top_tech_news_response is not None:
    #     tech_news_list = top_tech_news_response['articles'][:6]
    #     for news in tech_news_list:
    #         tech_news.append({
    #             'author': 'anonymous' if news['author'] is None else news['author'],
    #             'title': news['title'],
    #             'description': news['description'],
    #             'url': news['url'],
    #             'imageUrl': news['urlToImage'],
    #             'publishedAt': news['publishedAt']
    #         })

    # if top_sports_news_response is not None:
    #     sports_news_list = top_sports_news_response['articles'][4:10]
    #     for news in sports_news_list:
    #         sports_news.append({
    #             'author': 'anonymous' if news['author'] is None else news['author'],
    #             'title': news['title'],
    #             'description': news['description'],
    #             'url': news['url'],
    #             'imageUrl': news['urlToImage'],
    #             'publishedAt': news['publishedAt']
    #         })

    context = {
        'featured': featured_news,
        'business': business_news,
        'technology': tech_news,
        'sports': sports_news
    }

    return render(request, 'news/index.html', context=context)


def featured_news_detail(request, slug):
    return render(request, 'news/featured_news_detail.html')
