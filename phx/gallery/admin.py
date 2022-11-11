import logging

from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.utils.html import format_html
from easy_thumbnails.files import get_thumbnailer

from phx.admin import phx_admin

from .models import Gallery, Image, Thumbnail

logger = logging.getLogger(__name__)


class ImageAdmin(admin.StackedInline):
    model = Image
    readonly_fields = ['current_image']
    extra = 1

    def current_image(self, obj):
        thumbnailer = get_thumbnailer(obj.image)
        thumbnail_options = {'size': (200, 200)}
        return format_html('<img src="/media/{0}" />'.format(
            thumbnailer.get_thumbnail(thumbnail_options)))


class ThumbnailAdmin(admin.StackedInline):
    model = Thumbnail
    readonly_fields = ['current_image']

    def current_image(self, obj):
        thumbnailer = get_thumbnailer(obj.image)
        thumbnail_options = {'size': (200, 200)}
        return format_html('<img src="/media/{0}" />'.format(
            thumbnailer.get_thumbnail(thumbnail_options)))


class GalleryAdmin(admin.ModelAdmin):
    list_display = [
        'get_thumbnail',
        'title',
        'created_date',
        'event_date',
        'author',
        'image_count',
        'get_reorder_images_link',
    ]
    list_display_links = ['get_thumbnail', 'title']
    list_select_related = ['author', 'thumbnail']
    list_prefetch_related = ['images']
    search_fields = ['title']
    readonly_fields = ['slug']
    ordering = ['-created_date']
    exclude = ['author']
    inlines = [ThumbnailAdmin, ImageAdmin]

    def image_count(self, obj):
        return obj.images.count()

    def get_thumbnail(self, obj):
        try:
            thumbnailer = get_thumbnailer(obj.thumbnail.image)
            thumbnail_options = {'size': (100, 100)}
            return format_html('<img src="/media/{0}" />'.format(
                thumbnailer.get_thumbnail(thumbnail_options)))
        except Exception as e:
            logger.warning("Gallery admin error: '{}'".format(e))

    get_thumbnail.short_description = 'thumbnail'

    # add custom link to gallery image reordering
    def get_reorder_images_link(self, obj):
        return format_html(
            '<a href="../image/?gallery={}">Reorder images</a>'.format(obj.id))

    get_reorder_images_link.short_description = 'Reorder images'

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class ImageOrderAdmin(OrderableAdmin, admin.ModelAdmin):
    list_display = [
        'get_image',
        'caption',
        'order',
    ]
    list_editable = (
        'order',
        'caption',
    )
    list_display_links = None
    ordering_field = 'order'
    readonly_fields = ('order', )

    def changelist_view(self, request, extra_context=None):
        extra_context = {
            'title': 'Drag "order" to reorder images for this gallery'
        }
        return super(ImageOrderAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )

    def get_image(self, obj):
        thumbnailer = get_thumbnailer(obj.image)
        thumbnail_options = {'size': (100, 100)}
        return format_html('<img src="/media/{0}" />'.format(
            thumbnailer.get_thumbnail(thumbnail_options)))

    get_image.short_description = 'Image'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        gallery_id = request.GET.get('gallery')
        qs = super().get_queryset(request)
        return qs.filter(gallery_id=gallery_id)

    # hide link from admin home page
    def has_module_permission(self, request):
        return False


phx_admin.register(Gallery, GalleryAdmin)
phx_admin.register(Image, ImageOrderAdmin)
