from django.db import models
from authentication.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from imageBase.models import ImageModel


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64)
    about = models.TextField(default="")
    phone = models.CharField(max_length=18, null=True, default=None)
    image = models.ForeignKey(ImageModel, on_delete=models.PROTECT, null=True, blank=True)


@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

    else:
        try:
            instance.profile.save()

        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)
