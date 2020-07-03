from django.db import models
from django.utils import timezone

from people.models import User
from imageBase.models import ImageModel


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tittle = models.CharField(max_length=255)
    description = models.TextField()
    seen = models.PositiveIntegerField(default=0)
    condition = models.CharField(
        max_length=255,
        choices=(
            ("old", "Б/у"),
            ("new", "Новый")), default="old")
    price = models.PositiveIntegerField()
    tags = models.CharField(max_length=255, blank=True)
    images = models.ManyToManyField(ImageModel)
    avatar = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    phone = models.BooleanField(default=False)
    email = models.BooleanField(default=False)
    vk = models.BooleanField(default=False)
    facebook = models.BooleanField(default=False)
    twitter = models.BooleanField(default=False)
    odnoklassniki = models.BooleanField(default=False)
    telegram = models.BooleanField(default=False)
    whatsapp = models.BooleanField(default=False)
    viber = models.BooleanField(default=False)
