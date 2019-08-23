from django.contrib import admin

from .models import Image, Category, Trip, Cover



class ImageInLine(admin.StackedInline):
    model = Image
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]
    list_display = ('title', 'priority')
    search_fields = ['title', 'description']


class TripAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]
    list_display = ('title', 'priority')
    search_fields = ['title', 'description']


class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'trip', 'cols', 'rows')
    list_filter = ['category', 'trip']
    search_fields = ['title', 'description']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Trip, TripAdmin)

admin.site.register(Image, ImageAdmin)
admin.site.register(Cover)