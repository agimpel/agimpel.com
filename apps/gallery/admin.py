from django.contrib import admin

from .models import Image, Category, Trip



class ImageInLine(admin.StackedInline):
    model = Image
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]


class TripAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]



admin.site.register(Category, CategoryAdmin)
admin.site.register(Trip, TripAdmin)

admin.site.register(Image)