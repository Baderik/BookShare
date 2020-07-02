from django.core.files.base import ContentFile
from django.db import models

from io import BytesIO

from PIL import Image


class ImageModel(models.Model):
    image = models.ImageField(upload_to="img/")

    def save(self, *args, **kwargs):
        filename = ".".join(self.image.name.split(".")[:-1]) + ".jpg"
        image = Image.open(self.image)

        image = image.convert("RGB")
        image_io = BytesIO()

        image.save(image_io, format='JPEG', quality=70)
        self.image.save(filename, ContentFile(image_io.getvalue()), save=False)

        super(ImageModel, self).save(*args, **kwargs)
