from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify


from django.utils.timezone import now
from django.urls import reverse


User = get_user_model()

# Create your models here.


class FeaturedNews(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.CharField(max_length=50, blank=True, null=True, default='Anonymous')
    description = models.CharField(max_length=400)
    content = models.TextField()
    category = models.CharField(max_length=20)
    url = models.URLField(max_length=400)
    image_url = models.URLField(
        max_length=400, null=True, default='/static/images/register_background.jpg')
    published_date = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(FeaturedNews, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("news:featured_news_detail", kwargs={"slug": self.slug})


class Timestamp(models.Model):
    creationDate = models.DateTimeField(default=now)

    def __str__(self) -> str:
        return f'{self.creationDate}'

# class News(models.Model):
#     title = models.CharField(max_length=400)
#       slug = models.SlugField(max_length=400, unique=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)


# class Comments(models.Model):
#     pass
