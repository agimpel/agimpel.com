from django.db import models
from django.conf import settings
from django.utils import timezone

import os
import uuid
import logging
from PIL import Image as pil_image
from exiffield.fields import ExifField
from slugify import slugify

logger = logging.getLogger("django")

def scramble_uploaded_filename(instance, filename):
    extension = filename.split(".")[-1]
    
    if isinstance(instance, Image):
        uid = instance.slug_uid
        prefix = 'gallery/images'
    else:
        uid = uuid.uuid4()
        prefix = 'gallery/covers'
    return "{}/{}.{}".format(prefix, uid, extension)


def create_thumbnail(instance, input_image, thumbnail_size=(256, 256)):
    if not input_image or input_image == "":
        return

    image = pil_image.open(input_image)

    # use PILs thumbnail method; use anti aliasing to make the scaled picture look good
    image.thumbnail(thumbnail_size, pil_image.ANTIALIAS)

    filename = scramble_uploaded_filename(instance, os.path.basename(input_image.name))
    arrdata = filename.split(".")
    # extension is in the last element, pop it
    extension = arrdata.pop()
    basename = "".join(arrdata)
    # add _thumb to the filename
    new_filename = basename + "_thumb." + extension

    # save the image in MEDIA_ROOT and return the filename
    image.save(os.path.join(settings.MEDIA_ROOT, new_filename))

    return new_filename




class Category(models.Model):
    title = models.CharField("Title", max_length=200)
    slug = models.SlugField("Slug", max_length=40)
    description = models.CharField("Description", max_length=2000)
    cover = models.ImageField("Cover", upload_to=scramble_uploaded_filename, blank=True, null=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.cover.delete(save=False)
        for image in self.images.all(): image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"




class Trip(models.Model):
    title = models.CharField("Title", max_length=200)
    slug = models.SlugField("Slug", max_length=40)
    description = models.CharField("Description", max_length=2000)
    cover = models.ImageField("Cover", upload_to=scramble_uploaded_filename, blank=True, null=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.cover.delete(save=False)
        for image in self.images.all(): image.delete()
        super().delete(*args, **kwargs)





class Image(models.Model):
    title = models.CharField("Title", max_length=200)
    description = models.CharField("Description", max_length=2000)
    slug = models.SlugField(editable=False)
    src = models.ImageField("Image", upload_to=scramble_uploaded_filename)
    exif = ExifField(source='src')
    date = models.DateTimeField('Date', default=timezone.now)

    # related models
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE, blank=True, null=True)
    trip = models.ForeignKey(Trip, related_name='images', on_delete=models.CASCADE, blank=True, null=True)

    # thumbnail
    thumbnail = models.ImageField(editable=False)

    slug_uid = uuid.uuid4()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # generate and set thumbnail
        self.slug = slugify(self.title)
        self.thumbnail = create_thumbnail(self, self.src)

        # force update as we just changed something
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.src.delete(save=False)
        self.thumbnail.delete(save=False)

        # force update as we just changed something
        super().delete(*args, **kwargs)
