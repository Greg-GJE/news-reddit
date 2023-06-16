# pylint: disable=no-member

from django.db import models
from django.contrib.auth import get_user_model

from PIL import Image

# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            # convert to rgb
            rgb_image = img.convert('RGB')
            rgb_image.save(self.image.path)


    def __str__(self) -> str:
        return f'{self.user.username} Profile'
