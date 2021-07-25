from django.contrib import admin

from .models import Image, Category, Portfolio, Trip, Cover, Background



class ImageInLine_Portfolio(admin.StackedInline):
    model = Image
    readonly_fields = ['title', 'image_tag']
    fields = ('title', 'image_tag', 'portfolio_cols', 'portfolio_rows')
    extra = 1

class ImageInLine_Category(admin.StackedInline):
    model = Image
    readonly_fields = ['title', 'image_tag']
    fields = ('title', 'image_tag', 'category_cols', 'category_rows')
    extra = 1

class ImageInLine_Trip(admin.StackedInline):
    model = Image
    readonly_fields = ['title', 'image_tag']
    fields = ('title', 'image_tag', 'trip_cols', 'trip_rows')
    extra = 1

class PortfolioAdmin(admin.ModelAdmin):
    inlines = [ImageInLine_Portfolio]
    list_display = ('title', 'priority')
    search_fields = ['title', 'description']

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ImageInLine_Category]
    list_display = ('title', 'priority')
    search_fields = ['title', 'description']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj: form.base_fields['cover'].queryset = obj.images.all()
        return form


class TripAdmin(admin.ModelAdmin):
    inlines = [ImageInLine_Trip]
    list_display = ('title', 'priority', 'date')
    search_fields = ['title', 'description', 'date']
    ordering = ('-date',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj: form.base_fields['cover'].queryset = obj.images.all()
        return form


class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'portfolio', 'category', 'trip', 'exif_date', 'image_tag')
    list_filter = ['category', 'trip']
    search_fields = ['title', 'description']
    readonly_fields = ['image_tag', 'slug', 'upload_date']
    ordering = ('-exif_date',)

    fieldsets = (
        (None, {
           'fields': ('title', 'description', 'slug', 'upload_date', 'image_tag', 'src', 'photostream_cols', 'photostream_rows')
        }),
        ('Relations', {
            'fields': (('portfolio', 'portfolio_cols', 'portfolio_rows', 'portfolio_priority'), ('category', 'category_cols', 'category_rows', 'category_priority'), ('trip', 'trip_cols', 'trip_rows', 'trip_priority'))
        }),
        ('EXIF', {
            'fields': ('exif_model', 'exif_focallength', 'exif_aperture', 'exif_shutterspeed', 'exif_iso', 'exif_date'),
        }),
    )


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Trip, TripAdmin)

admin.site.register(Image, ImageAdmin)
admin.site.register(Cover)
admin.site.register(Background)