from django.db import models
from django.conf import settings
from django.utils.timezone import make_aware
from django.utils.html import mark_safe

import os
import uuid
import logging
import datetime
from PIL import Image as pil_image
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
    position = models.CharField(max_length=200, default="50% 50%")

    # original image (not saved)
    src = models.ImageField("Image", upload_to=None)

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

        if self.src:
            width = self.src.width
            height = self.src.height
            htw_ratio = height/width

            self.thumbnail_1x = resize_image(self, self.src, size=(COVER_WIDTH, htw_ratio*COVER_WIDTH), name_suffix='1x')
            self.thumbnail_2x = resize_image(self, self.src, size=(2*COVER_WIDTH, 2*htw_ratio*COVER_WIDTH), name_suffix='2x')

            self.src.delete(save=False)

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.src.delete(save=False)
        self.thumbnail_1x.delete(save=False)
        self.thumbnail_2x.delete(save=False)
        super().delete(*args, **kwargs)



class Portfolio(models.Model):
    title = models.CharField("Title", max_length=200)
    slug = models.SlugField("Slug", max_length=40)
    description = models.CharField("Description", max_length=2000, blank=True, null=True)
    cover = models.ForeignKey(Cover, related_name='portfoliocover', on_delete=models.CASCADE, blank=True, null=True)
    priority = models.IntegerField("Priority", blank=True, null=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Portfolios"




class Category(models.Model):
    title = models.CharField("Title", max_length=200)
    slug = models.SlugField("Slug", max_length=40)
    description = models.CharField("Description", max_length=2000, blank=True, null=True)
    cover = models.ForeignKey('Image', related_name='categorycover', on_delete=models.CASCADE, blank=True, null=True)
    priority = models.IntegerField("Priority", blank=True, null=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
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
    upload_date = models.DateTimeField(auto_now_add=True)

    # position of image in grid
    portfolio_cols = models.IntegerField("Col Span", default=1)
    portfolio_rows = models.IntegerField("Row Span", default=1)
    category_cols = models.IntegerField("Col Span", default=1)
    category_rows = models.IntegerField("Row Span", default=1)
    trip_cols = models.IntegerField("Col Span", default=1)
    trip_rows = models.IntegerField("Row Span", default=1)

    # related models
    portfolio = models.ForeignKey(Portfolio, related_name='images', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE, blank=True, null=True)
    trip = models.ForeignKey(Trip, related_name='images', on_delete=models.CASCADE, blank=True, null=True)

    # base image (not saved)
    src = models.ImageField("New image", upload_to=None, blank=True)

    # processed images
    thumbnail_1x = models.ImageField(editable=False)
    thumbnail_2x = models.ImageField(editable=False)
    picture = models.ImageField(editable=False)

    # scraped EXIF data
    exif_model = models.CharField("Model", max_length=100, blank=True, null=True)
    exif_focallength = models.CharField("Focal Length", max_length=100, blank=True, null=True)
    exif_iso = models.CharField("ISO", max_length=100, blank=True, null=True)
    exif_shutterspeed = models.CharField("Shutter Speed", max_length=100, blank=True, null=True)
    exif_aperture = models.CharField("Aperture", max_length=100, blank=True, null=True)
    exif_date = models.DateTimeField("Date", blank=True, null=True)

    # uid
    slug_uid = models.CharField(editable=False, default="", max_length=2000)


    def image_tag(self):
        return mark_safe('<a href="%s"><img src="%s" width="150"></a>' % (self.picture.url, self.thumbnail_1x.url))
    image_tag.short_description = 'Current image'


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        # generate and set thumbnail
        self.slug = slugify(self.title)
        if not self.slug_uid:
            self.slug_uid = uuid.uuid4()


        if self.src:

            width = self.src.width
            height = self.src.height
            htw_ratio = height/width
            multiplier = 2

            self.thumbnail_1x = resize_image(self, self.src, size=(multiplier*THUMBNAIL_WIDTH, multiplier*htw_ratio*THUMBNAIL_WIDTH), name_suffix='1x')
            self.thumbnail_2x = resize_image(self, self.src, size=(2*multiplier*THUMBNAIL_WIDTH, 2*multiplier*htw_ratio*THUMBNAIL_WIDTH), name_suffix='2x')
            self.picture = resize_image(self, self.src, size=(PICTURE_WIDTH, htw_ratio*PICTURE_WIDTH), name_suffix='full')

            # scrape the EXIF data
            img_exif = pil_image.open(self.src).getexif()
            if img_exif is None:
                self.exif_model = "?"
                self.exif_focallength = "?"
                self.exif_iso = "?"
                self.exif_shutterspeed = "?"
                self.exif_aperture = "?"
                self.exif_date = None
            else:
                self.exif_model = img_exif.get(272)
                self.exif_focallength = img_exif.get(37386)
                self.exif_iso = img_exif.get(34855)
                self.exif_shutterspeed = img_exif.get(33434) if img_exif.get(33434) > 1 else "1/"+str(int(1/img_exif.get(33434)))
                self.exif_aperture = img_exif.get(33437)
                self.exif_date = make_aware(datetime.datetime.strptime(img_exif.get(36867), '%Y:%m:%d %H:%M:%S'))

            # remove the source image so it is no longer available
            self.src.delete(save=False)

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.src.delete(save=False)
        self.thumbnail_1x.delete(save=False)
        self.thumbnail_2x.delete(save=False)
        self.picture.delete(save=False)

        super().delete(*args, **kwargs)