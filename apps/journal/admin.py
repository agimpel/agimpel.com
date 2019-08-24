from django.contrib import admin

from .models import Entry, Category, Tag, Description, Link


class TagInLine(admin.TabularInline):
    model = Tag
    extra = 1

class CategoriesInLine(admin.TabularInline):
    model = Entry.categories.through
    extra = 1

class DescriptionsInLine(admin.TabularInline):
    model = Description
    extra = 1

class LinksInLine(admin.TabularInline):
    model = Link
    extra = 1

class EntryAdmin(admin.ModelAdmin):
    inlines = [DescriptionsInLine, LinksInLine, CategoriesInLine]
    exclude = ('categories',)
    list_display = ('title', 'tag_list', 'show', 'gallery')
    search_fields = ['title', 'description', 'categories']
    list_filter = ['categories']

    def tag_list(self, obj):
        return ", ".join([str(p) for p in obj.categories.all()])

class CategoryAdmin(admin.ModelAdmin):
    inlines = [TagInLine]
    list_display = ('title',)
    search_fields = ['title',]

class TagAdmin(admin.ModelAdmin):
    inlines = [TagInLine]
    list_display = ('title',)
    search_fields = ['title',]


admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)