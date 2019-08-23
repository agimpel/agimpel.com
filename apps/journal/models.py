from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.gallery.models import Trip

from slugify import slugify







class Category(models.Model):
    title = models.CharField("Title", max_length=200)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    title = models.CharField("Tag", max_length=200)
    slug = models.SlugField(editable=False)
    parent = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.parent.title + ": " + self.title





class Entry(models.Model):
    title = models.CharField("Title", max_length=200)
    short_title = models.CharField("Short title", max_length=40)
    slug = models.SlugField(editable=False)
    description = models.TextField("Description", max_length=2000, blank=True, null=True)
    link = models.URLField("Link", max_length=200, blank=True, null=True)
    show = models.BooleanField("Show", default=True)
    order = models.IntegerField("Priority", blank=True, null=True)

    categories = models.ManyToManyField(Tag, related_name='entries')

    gallery = models.OneToOneField(Trip, related_name='journal', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Entries"
