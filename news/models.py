# pylint: disable=no-member

from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify


from django.utils.timezone import now
from django.urls import reverse

from PIL import Image


User = get_user_model()

# Create your models here.


# This will behave as cache for FeaturedNews
class FeaturedNews(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.CharField(
        max_length=50, blank=True, null=True, default='Anonymous')
    description = models.CharField(max_length=400)
    content = models.TextField()
    category = models.CharField(max_length=20)
    url = models.URLField(max_length=400)
    image_url = models.URLField(
        max_length=400, null=True, default='/static/images/register_background.jpg')
    published_date = models.DateTimeField(default=now)

    class Meta:
        indexes = [
            models.Index(fields=['slug'])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.author is None:
            self.author = 'Anonymous'
        if self.image_url is None:
            self.image_url = '/static/images/register_background.jpg'
        super(FeaturedNews, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("news:featured_news_detail", kwargs={"slug": self.slug})


class Timestamp(models.Model):
    creationDate = models.DateTimeField(default=now)

    def __str__(self) -> str:
        return f'{self.creationDate}'



class CommunityNews(models.Model):

    CATEGORIES = (
        ("business", "Business"),
        ("entertainment", "Entertainment"),
        ("sports", "Sports"),
        ("lifestyle", "Lifestyle"),
        ("technology", "Technology"),
        ("others", "Others")
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='news')
    banner = models.ImageField(
        default='default_news.jpg', upload_to='community_news')
    description = models.TextField(max_length=400)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="lifestyle")

    def get_total_upvotes(self):
        return self.upvotes.users.count()

    def get_total_downvotes(self):
        return self.downvotes.users.count()

    def get_votes(self):
        return self.get_total_upvotes() - self.get_total_downvotes()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(CommunityNews, self).save(*args, **kwargs)

        banner_image = Image.open(self.banner.path)

        if banner_image.height > 600 or banner_image.width > 800:
            output_size = (600, 800)
            banner_image.thumbnail(output_size)

            banner_image.save(self.banner.path)


class Comment(models.Model):
    description = models.CharField(max_length=150, null=False, blank=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    news = models.ForeignKey(
        CommunityNews, on_delete=models.CASCADE, related_name='comments')

    def __str__(self) -> str:
        return f'{self.description}'


class UpVote(models.Model):
    news = models.OneToOneField(
        CommunityNews, related_name='upvotes', on_delete=models.CASCADE)
    users = models.ManyToManyField(
        User, related_name='requirement_news_upvotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.news.title}'


class DownVote(models.Model):
    news = models.OneToOneField(
        CommunityNews, related_name='downvotes', on_delete=models.CASCADE)
    users = models.ManyToManyField(
        User, related_name='requirement_news_downvotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.news.title}'
