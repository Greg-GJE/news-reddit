from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Comments(models.Model):
    pass
