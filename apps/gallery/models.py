from django.db import models
from django.conf import settings
from django.utils import timezone

import os
import uuid
import logging
from PIL import Image as pil_image
from exiffield.fields import ExifField
from slugify import slugify

logger = logging.getLogger("agimpel.gallery.models")

THUMBNAIL_WIDTH = 300
COVER_WIDTH = 960
PICTURE_WIDTH = 1920


def scramble_uploaded_filename(instance, filename):
    extension = filename.split(".")[-1]
    
    if isinstance(instance, Image):
        uid = instance.slug_uid
        prefix = 'gallery/images/'
    elif isinstance(instance, Cover):
        uid = instance.slug_uid
        prefix = 'gallery/covers/'
    else:
        uid = uuid.uuid4()
        prefix = 'gallery/others/'
    return "{}{}.{}".format(prefix, uid, extension)


def resize_image(instance, input_image, size=(256, 256), name_suffix=''):
    if not input_image or input_image == "":
        return

    size = tuple(map(round, size))
    try:
        image = pil_image.open(input_image)
    except:
        image = pil_image.open(os.path.join(settings.BASE_DIR, input_image.url.strip("/")))

    # use PILs resize method
    image = image.resize(size, pil_image.ANTIALIAS)

    filename = scramble_uploaded_filename(instance, os.path.basename(input_image.name))
    arrdata = filename.split(".")
    # extension is in the last element, pop it
    extension = arrdata.pop()
    basename = "".join(arrdata)
    # add _thumb to the filename
    new_filename = basename + "_" + name_suffix + "." + extension

    # save the image in MEDIA_ROOT and return the filename
    image.save(os.path.join(settings.MEDIA_ROOT, new_filename), quality=95, optimize=True)

    return new_filename


class Cover(models.Model):
    slug = models.SlugField("Slug", max_length=200)
    src = models.ImageField("Image", upload_to=scramble_uploaded_filename)
    position = models.CharField(max_length=200, default="50% 50%")
    # processed images
    thumbnail_1x = models.ImageField(editable=False)
    thumbnail_2x = models.ImageField(editable=False)

    # uid
    slug_uid = models.CharField(editable=False, default="", max_length=2000)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        # generate and set thumbnail
        if not self.slug_uid:
            self.slug_uid = uuid.uuid4()

        width = self.src.width
        height = self.src.height
        htw_ratio = height/width

        self.thumbnail_1x = resize_image(self, self.src, size=(COVER_WIDTH, htw_ratio*COVER_WIDTH), name_suffix='1x')
        self.thumbnail_2x = resize_image(self, self.src, size=(2*COVER_WIDTH, 2*htw_ratio*COVER_WIDTH), name_suffix='2x')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.src.delete(save=False)
        self.thumbnail_1x.delete(save=False)
        self.thumbnail_2x.delete(save=False)
        super().delete(*args, **kwargs)



class Category(models.Model):
    title = models.CharField("Title", max_length=200)
    slug = models.SlugField("Slug", max_length=40)
    description = models.CharField("Description", max_length=2000, blank=True, null=True)
    cover = models.ForeignKey(Cover, related_name='categorycover', on_delete=models.CASCADE, blank=True, null=True)
    priority = models.IntegerField("Priority", blank=True, null=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        for image in self.images.all(): image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"




class Trip(models.Model):
    title = models.CharField("Title", max_length=200)
    slug = models.SlugField("Slug", max_length=40)
    description = models.CharField("Description", max_length=2000, blank=True, null=True)
    cover = models.ForeignKey('Image', related_name='tripcover', on_delete=models.CASCADE, blank=True, null=True)
    show = models.BooleanField("Show", default=True)
    priority = models.IntegerField("Priority", blank=True, null=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        for image in self.images.all(): image.delete()
        super().delete(*args, **kwargs)





class Image(models.Model):
    title = models.CharField("Title", max_length=200)
    description = models.CharField("Description", max_length=2000, blank=True, null=True)
    slug = models.SlugField(editable=False)
    src = models.ImageField("Image", upload_to=scramble_uploaded_filename)
    exif = ExifField(source='src')
    cols = models.IntegerField("Col Span", default=1)
    rows = models.IntegerField("Row Span", default=1)

    # related models
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE, blank=True, null=True)
    trip = models.ForeignKey(Trip, related_name='images', on_delete=models.CASCADE, blank=True, null=True)

    # processed images
    thumbnail_1x = models.ImageField(editable=False)
    thumbnail_2x = models.ImageField(editable=False)
    picture = models.ImageField(editable=False)

    # uid
    slug_uid = models.CharField(editable=False, default="", max_length=2000)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # generate and set thumbnail
        self.slug = slugify(self.title)
        if not self.slug_uid:
            self.slug_uid = uuid.uuid4()

        width = self.src.width
        height = self.src.height
        htw_ratio = height/width
        multiplier = max(self.rows, self.cols)

        self.thumbnail_1x = resize_image(self, self.src, size=(multiplier*THUMBNAIL_WIDTH, multiplier*htw_ratio*THUMBNAIL_WIDTH), name_suffix='1x')
        self.thumbnail_2x = resize_image(self, self.src, size=(2*multiplier*THUMBNAIL_WIDTH, 2*multiplier*htw_ratio*THUMBNAIL_WIDTH), name_suffix='2x')
        self.picture = resize_image(self, self.src, size=(PICTURE_WIDTH, htw_ratio*PICTURE_WIDTH), name_suffix='full')

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.src.delete(save=False)
        self.thumbnail_1x.delete(save=False)
        self.thumbnail_2x.delete(save=False)
        self.picture.delete(save=False)

        super().delete(*args, **kwargs)


    def _exif(self, key):
        try:
            data = self.exif[key]['val']
        except:
            data = "?"
        if not data:
            data = "unknown"
        return data

    def exif_model(self):
        return self._exif('Model')

    def exif_focallength(self):
        return self._exif('FocalLength')
    
    def exif_iso(self):
        return self._exif('ISO')

    def exif_shutterspeed(self):
        return self._exif('ShutterSpeedValue')

    def exif_aperture(self):
        return self._exif('ApertureValue')
