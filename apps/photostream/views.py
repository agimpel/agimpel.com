from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.template import loader
from django.urls import reverse
import logging

from apps.gallery.models import Image

logger = logging.getLogger("agimpel.photostream.views")


class IndexView(generic.TemplateView):
    template_name = 'photostream/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Image.objects.all().order_by('-exif_date')
        context['title'] = 'Photostream'
        context['nav_title'] = [['photostream', None]]
        return context



class PhotoView(generic.DetailView):
    template_name = 'gallery/image.html'
    model = Image
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        img = Image.objects.get(pk=self.kwargs['pk'])
        slug = img.slug if len(img.slug) < 20 else img.slug[0:20] + "..."

        context['title'] = img.title
        context['nav_title'] = [['photostream', reverse('photostream:index')], [slug, None]]
        return context
