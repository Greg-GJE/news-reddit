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

    # getting the country from where the request is made
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    country_code = fetch_country_code()

    if country_code is None:
        country_code = 'us'


    # news_api_client = NewsApiClient(api_key=settings.NEWSAPI_KEY)

    # top_news = news_api_client.get_top_headlines(language='en', country=country_code.lower())

    # featured_news = top_news['articles'][0]


    return render(request, 'news/index.html')
