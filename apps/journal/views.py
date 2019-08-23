from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.template import loader
from django.urls import reverse

from .models import Entry


class IndexView(generic.TemplateView):
    template_name = 'journal/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Journal'
        context['nav_title'] = [['journal', None]]
        return context


class EntryView(generic.DetailView):
    template_name = 'journal/entry.html'
    model = Entry
    context_object_name = 'entry'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = Entry.objects.get(slug=self.kwargs['slug'])
        context['title'] = entry.title
        context['nav_title'] = [['journal', reverse('journal:index')], [entry.slug, None]]
        return context
