from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.template import loader

from .models import Category, Trip, Image


class IndexView(generic.ListView):
    template_name = 'gallery/index.html'
    context_object_name = 'list'


class CategoryView(generic.ListView):
    template_name = 'gallery/category.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.category.images.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context



class TripView(generic.ListView):
    template_name = 'gallery/trip.html'

    def get_queryset(self):
        self.trip = get_object_or_404(Trip, slug=self.kwargs['slug'])
        return self.trip.images.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip'] = self.trip
        return context




class ImageView(generic.DetailView):
    template_name = 'gallery/image.html'
    model = Image
    context_object_name = 'image'