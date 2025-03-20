from django.shortcuts import render
from django.views import generic
from django.urls import reverse
import logging

from .models import Tag, Project


logger = logging.getLogger("agimpel.projects.views")


class IndexView(generic.TemplateView):
    template_name = 'projects/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all().order_by('-order')
        context['tags'] = Tag.objects.all().order_by('-order')
        context['title'] = 'Projects'
        context['nav_title'] = [['projects', None]]
        return context
    


class ProjectView(generic.DetailView):
    template_name = 'projects/detail.html'
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(slug=self.kwargs['slug'])
        context['project'] = project
        context['title'] = project.name
        context['nav_title'] = [['projects', reverse('projects:index')], [project.slug, None]]
        return context