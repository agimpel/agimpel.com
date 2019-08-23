from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.template import loader
from django.urls import reverse
import logging

from .models import Category, Trip, Image

logger = logging.getLogger("django")


class IndexView(generic.TemplateView):
    template_name = 'gallery/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['trips'] = Trip.objects.all()
        context['trips_shown'] = []
        context['trips_hidden'] = []
        for trip in context['trips']:
            if trip.show:
                context['trips_shown'].append(trip)
            else: 
                context['trips_hidden'].append(trip)
        context['trips_shown'] 
        context['title'] = 'Gallery'
        context['nav_title'] = [['gallery', None]]
        return context


class CategoryView(generic.ListView):
    template_name = 'gallery/category.html'
    context_object_name = 'images'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.category.images.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['title'] = self.category.title
        context['nav_title'] = [['gallery', reverse('gallery:index')], [self.category.slug, None]]
        return context



class TripView(generic.ListView):
    template_name = 'gallery/trip.html'
    context_object_name = 'images'

    def get_queryset(self):
        self.trip = get_object_or_404(Trip, slug=self.kwargs['slug'])
        return self.trip.images.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip'] = self.trip
        context['title'] = self.trip.title
        context['nav_title'] = [['gallery', reverse('gallery:index')], [self.trip.slug, None]]
        context['journal_available'] = False
        logger.info(hasattr(self.trip, 'journal'))
        if hasattr(self.trip, 'journal'):
            logger.info("Here")
            context['journal_available'] = True
            context['journal_link'] = reverse('journal:entry', args=(self.trip.journal.slug,))
        return context




class ImageView(generic.DetailView):
    template_name = 'gallery/image.html'
    model = Image
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        img = Image.objects.get(pk=self.kwargs['pk'])
        context['title'] = img.title
        if img.category:
            context['nav_title'] = [['gallery', reverse('gallery:index')], [img.category.slug, reverse('gallery:category', args=(img.category.slug,))], ['image', None]]
        elif img.trip:
            context['nav_title'] = [['gallery', reverse('gallery:index')], [img.trip.slug, reverse('gallery:trip', args=(img.trip.slug,))], ['image', None]]
        else:
            context['nav_title'] = [['gallery', reverse('gallery:index')], ['image', None]]
        return context
