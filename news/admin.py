from django.contrib import admin

# Register your models here.
from .models import FeaturedNews, Timestamp, Comment, CommunityNews, UpVote, DownVote

admin.site.register(FeaturedNews)
admin.site.register(Timestamp)
admin.site.register(Comment)
admin.site.register(CommunityNews)
admin.site.register(UpVote)
admin.site.register(DownVote)

