from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.template import loader
from django.urls import reverse

from .models import Category, Trip, Image


class IndexView(generic.TemplateView):
    template_name = 'gallery/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['trips'] = Trip.objects.all()
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
