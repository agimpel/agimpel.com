from django.contrib import admin

from .models import Project, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ['name', 'order']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ['name', 'order']


admin.site.register(Tag, TagAdmin)
admin.site.register(Project, ProjectAdmin)