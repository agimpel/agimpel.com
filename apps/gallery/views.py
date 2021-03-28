from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.template import loader
from django.urls import reverse
import logging

from .models import Category, Trip, Image, Portfolio

logger = logging.getLogger("agimpel.gallery.views")


class IndexView(generic.TemplateView):
    template_name = 'gallery/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['portfolios'] = Portfolio.objects.all()
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


class PortfolioView(generic.ListView):
    template_name = 'gallery/portfolio.html'
    context_object_name = 'images'

    def get_queryset(self):
        self.portfolio = get_object_or_404(Portfolio, slug=self.kwargs['slug'])
        return self.portfolio.images.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolio'] = self.portfolio
        context['title'] = self.portfolio.title
        context['nav_title'] = [['gallery', reverse('gallery:index')], [self.portfolio.slug, None]]
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
        if hasattr(self.trip, 'journal'):
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
        slug = img.slug if len(img.slug) < 20 else img.slug[0:20] + "..."

        context['title'] = img.title
        context['nav_title'] = [['gallery', reverse('gallery:index')], [slug, None]]

        return context
