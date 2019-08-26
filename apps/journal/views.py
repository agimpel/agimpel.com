from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect
from django.http import Http404

from .forms import FilterForm
from .models import Entry, Category, Tag

import logging
logger = logging.getLogger("agimpel.journal.views")


def prepare_entries_datamatrix(entries, columns): 
    matrix = []
    for entry in entries:
        added_columns = []
        for column in columns:
            added_column = []
            if entry.categories.filter(category=column): added_column.extend(entry.categories.filter(category=column))
            for child in column.children.filter(show=False):
                if entry.categories.filter(category=child): added_column.extend(entry.categories.filter(category=child))
            added_columns.append(added_column)
        matrix.append([entry, added_columns])
    return matrix


def FilterRedirect(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['activity'] != "all" or form.cleaned_data['region'] != "all":
                query_activity = form.cleaned_data['activity']+"/" if form.cleaned_data['activity'] != "all" else ""
                query_region = form.cleaned_data['region']+"/" if form.cleaned_data['region'] != "all" else ""
                query = query_activity+query_region
                logger.info(query)
                url = reverse('journal:filter', args=[query])
            else:
                url = reverse('journal:index')
            return HttpResponseRedirect(url)
        else:
            raise Http404('Form is invalid.')
    else:
        raise Http404()


class IndexView(generic.TemplateView):
    template_name = 'journal/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entries'] = Entry.objects.all().order_by('-order', 'title')
        context['columns'] = Category.objects.filter(show=True).order_by('order', 'title')
        context['entries_datamatrix'] = prepare_entries_datamatrix(Entry.objects.all().order_by('-order', 'title'), Category.objects.filter(show=True).order_by('order', 'title'))
        context['title'] = 'Journal'
        context['filter_form'] = FilterForm()
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

        context['entries'] = entries.order_by('-order', 'title')
        context['columns'] = Category.objects.filter(show=True).order_by('order', 'title')
        context['entries_datamatrix'] = prepare_entries_datamatrix(entries.order_by('-order', 'title'), Category.objects.filter(show=True).order_by('order', 'title'))
        context['queries'] = required_tags
        context['queries_n'] = len(entries)
        context['title'] = 'Filter Results'
        context['nav_title'] = [['journal', reverse('journal:index')], ['filter results', None]]
        return context
