from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.template import loader
from django.urls import reverse
import logging

from .models import Photo

logger = logging.getLogger("agimpel.photostream.views")


class IndexView(generic.TemplateView):
    template_name = 'photostream/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.all().order_by('-date')
        context['title'] = 'Photostream'
        context['nav_title'] = [['photostream', None]]
        return context



class PhotoView(generic.DetailView):
    template_name = 'photostream/photo.html'
    model = Photo
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        img = Photo.objects.get(pk=self.kwargs['pk'])
        context['title'] = img.title
        context['nav_title'] = [['photostream', reverse('photostream:index')], ['image #'+self.kwargs['pk'], None]]
        return context
