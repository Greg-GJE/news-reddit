from django.shortcuts import render
from django.conf import settings
from newsapi import NewsApiClient
import json

import requests


def fetch_country_code():
    # getting the geolocation response
    geolocation_response = requests.get(settings.GEOLOCATION_API_URL, verify=False, timeout=10)

    if geolocation_response is not None and geolocation_response.content is not None:
        data = json.loads(geolocation_response.content)
        return data.get('country_code')

    return None

# Create your views here.
def index(request):

    country_code = fetch_country_code()

    if country_code is None:
        country_code = 'us'


    news_api_client = NewsApiClient(api_key=settings.NEWSAPI_KEY)

    top_news_response = news_api_client.get_top_headlines(language='en', country=country_code.lower())
    top_business_news_response = news_api_client.get_top_headlines(language='en', category='business')
    top_tech_news_response = news_api_client.get_top_headlines(language='en', category='technology')
    top_sports_news_response = news_api_client.get_top_headlines(language='en', category='sports')


    featured_news = []
    business_news = []
    tech_news = []
    sports_news = []

    if top_news_response is not None:
        featured_news_list = top_news_response['articles'][:6]
        for news in featured_news_list:
            featured_news.append({
              'author': 'anonymous' if news['author'] is None else news['author'],
              'title': news['title'],
              'description': news['description'],
              'url': news['url'],
              'imageUrl': news['urlToImage'],
              'publishedAt': news['publishedAt']
            })

    if top_business_news_response is not None:
        business_news_list = top_business_news_response['articles'][1:7]
        for news in business_news_list:
            business_news.append({
              'author': 'anonymous' if news['author'] is None else news['author'],
              'title': news['title'],
              'description': news['description'],
              'url': news['url'],
              'imageUrl': news['urlToImage'],
              'publishedAt': news['publishedAt']
            })

    if top_tech_news_response is not None:
        tech_news_list = top_tech_news_response['articles'][:6]
        for news in tech_news_list:
            tech_news.append({
              'author': 'anonymous' if news['author'] is None else news['author'],
              'title': news['title'],
              'description': news['description'],
              'url': news['url'],
              'imageUrl': news['urlToImage'],
              'publishedAt': news['publishedAt']
            })

    if top_sports_news_response is not None:
        sports_news_list = top_sports_news_response['articles'][4:10]
        for news in sports_news_list:
            sports_news.append({
              'author': 'anonymous' if news['author'] is None else news['author'],
              'title': news['title'],
              'description': news['description'],
              'url': news['url'],
              'imageUrl': news['urlToImage'],
              'publishedAt': news['publishedAt']
            })

    context = {
        'featured': featured_news,
        'business': business_news,
        'technology': tech_news,
        'sports': sports_news
    }


    return render(request, 'news/index.html', context=context)
