from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.template import loader
from django.urls import reverse

from .models import Entry, Category, Tag

import logging
logger = logging.getLogger("django")


def prepare_entries_datamatrix(entries, columns): 
    matrix = [[entry,] for entry in entries]
    for element in matrix:
        element.append([element[0].categories.filter(category=column) for column in columns])

    logger.info(matrix[0][1][0][0])
    return matrix



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


class FilterView(generic.ListView):
    template_name = 'journal/filter.html'

    def get_queryset(self):
        pass

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        filter_string = self.args[0][0:len(self.args[0])-1] if self.args[0][-1] is "/" else self.args[0]
        filter_map = [s.split(".") for s in filter_string.split("/")]

        required_tags = []
        for filter_group in filter_map:
            category = get_object_or_404(Category, slug=filter_group.pop(0))
            tag = get_object_or_404(Tag, slug=filter_group.pop(0), category=category)
            for child in filter_group:
                tag = get_object_or_404(Tag, slug=child, parent=tag)
            required_tags.append(tag)

        entries = Entry.objects.all()
        for tag in required_tags:
            entries = entries.filter(categories=tag)

        context['entries'] = entries
        context['columns'] = Category.objects.filter(show=True)
        context['entries_datamatrix'] = prepare_entries_datamatrix(entries, Category.objects.filter(show=True))
        context['queries'] = required_tags
        context['queries_n'] = len(entries)
        context['title'] = 'Filter Results'
        context['nav_title'] = [['journal', reverse('journal:index')], ['filter results', None]]
        return context
