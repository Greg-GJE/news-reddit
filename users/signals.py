from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile

import logging

logger = logging.getLogger("herokulogger")

user_model = get_user_model()

@receiver(post_save, sender=user_model)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=user_model)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except FileNotFoundError as error:
        logger.error("Profile found removed by the server %s", error)

