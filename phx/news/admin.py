from easy_thumbnails.files import get_thumbnailer
from django.utils.html import format_html
from phx.admin import phx_admin
from .models import (News, Thumbnail, Component, Editorial, Feature,
                     Quote, Image, ListItems)
from components.admin import (AbstractEditorialAdmin, AbstractFeatureAdmin,
                              AbstractListItemsAdmin, AbstractQuoteAdmin,
                              AbstractImageAdmin)
import nested_admin


class EditorialAdmin(AbstractEditorialAdmin):
    model = Editorial


class FeatureAdmin(AbstractFeatureAdmin):
    model = Feature


class ListItemsAdmin(AbstractListItemsAdmin):
    model = ListItems


class QuoteAdmin(AbstractQuoteAdmin):
    model = Quote


class ImageAdmin(AbstractImageAdmin):
    model = Image


class ComponentAdmin(nested_admin.NestedStackedInline):
    model = Component
    extra = 0
    inlines = [
        EditorialAdmin,
        FeatureAdmin,
        ListItemsAdmin,
        QuoteAdmin,
        ImageAdmin,
    ]
    sortable_field_name = 'order'


class ThumbnailAdmin(nested_admin.NestedStackedInline):
    model = Thumbnail
    readonly_fields = ['current_image']

    def current_image(self, obj):
        thumbnailer = get_thumbnailer(obj.image)
        thumbnail_options = {'size': (200, 200)}
        return format_html(
            '<img src="/media/{0}" />'.format(
                thumbnailer.get_thumbnail(thumbnail_options)
            )
        )


class NewsAdmin(nested_admin.NestedModelAdmin):
    list_display = ['current_image', 'title', 'created_date', 'author']
    list_display_links = ['current_image', 'title']
    exclude = ['author']
    inlines = [ThumbnailAdmin, ComponentAdmin]

    def current_image(self, obj):
        thumbnailer = get_thumbnailer(obj.thumbnail.image)
        thumbnail_options = {'size': (100, 100)}
        return format_html(
            '<img src="/media/{0}" />'.format(
                thumbnailer.get_thumbnail(thumbnail_options)
            )
        )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


phx_admin.register(News, NewsAdmin)
