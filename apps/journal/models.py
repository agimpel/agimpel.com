from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.gallery.models import Trip

from slugify import slugify
import uuid

import logging
logger = logging.getLogger("django")

def upload_icon(instance, filename):
    extension = filename.split(".")[-1]
    
    if isinstance(instance, Tag):
        uid = instance.category.slug + '_' + instance.slug
        prefix = 'journal/icons/'
    else:
        uid = uuid.uuid4()
        prefix = 'journal/others/'
    return "{}{}.{}".format(prefix, uid, extension)



class Category(models.Model):
    title = models.CharField("Title", max_length=200)
    short_title = models.CharField("Short title", max_length=20)
    slug = models.SlugField(editable=False)
    show = models.BooleanField("Show", default=False)
    order = models.IntegerField("Order", default=99)
    parent = models.ForeignKey('Category', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    verbose = models.CharField("Verbosity", max_length=1, choices=(('I', 'icon only'), ('T', 'title only'), ('B', 'both'),), default='T')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return str(self.parent) + "." + self.short_title
        else:
            return self.short_title

    def name(self):
        return self.title

    def short_name(self):
        return self.short_title

    def shown_parent(self):
        if self.show:
            return self.slug
        else:
            return self.parent.shown_parent()


    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    title = models.CharField("Tag", max_length=200)
    short_title = models.CharField("Short tag", max_length=20)
    slug = models.SlugField(editable=False)
    category = models.ForeignKey(Category, related_name='tags', on_delete=models.CASCADE)
    parent = models.ForeignKey('Tag', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    icon = models.FileField("Icon", upload_to=upload_icon, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return str(self.parent) + "." + self.short_title
        else:
            return str(self.category) + "." + self.short_title

    def name(self):
        return self.title

    def short_name(self):
        return self.short_title

    def hierarchical_slug(self):
        if self.parent:
            return self.parent.hierarchical_slug() + "." + self.slug
        else:
            return self.category.slug + "." + self.slug

    def shown_category(self):
        return self.category.shown_parent()



class Entry(models.Model):
    title = models.CharField("Title", max_length=200)
    short_title = models.CharField("Short title", max_length=40)
    summary = models.TextField("Summary", max_length=2000)
    slug = models.SlugField(editable=False)
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



class Description(models.Model):
    title = models.CharField("Title", max_length=200)
    slug = models.SlugField(editable=False)
    text = models.TextField("Description", max_length=20000)
    entry = models.ForeignKey(Entry, related_name='descriptions', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.entry.title + "->" + self.title


class Link(models.Model):
    title = models.CharField("Title", max_length=200)
    slug = models.SlugField(editable=False)
    url = models.URLField("Link")
    entry = models.ForeignKey(Entry, related_name='links', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.entry.title + "->" + self.title
