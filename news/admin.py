from django.contrib import admin

# Register your models here.
from .models import FeaturedNews, Timestamp

admin.site.register(FeaturedNews)
admin.site.register(Timestamp)
