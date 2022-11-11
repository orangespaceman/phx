import logging

from components.models import (
    AbstractEditorial,
    AbstractEmbed,
    AbstractFeature,
    AbstractGallery,
    AbstractImage,
    AbstractListItem,
    AbstractListItems,
    AbstractProfile,
    AbstractProfileMember,
    AbstractQuote,
    AbstractResult,
    AbstractTable,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from gallery.models import Gallery as GalleryModel
from results.models import Result as ResultModel

logger = logging.getLogger(__name__)


def generate_slug(instance):
    if instance.parent:
        return '{0}{1}/'.format(instance.parent.slug, slugify(instance.title))
    else:
        return '/{0}/'.format(slugify(instance.title))


class Page(models.Model):
    order = models.IntegerField(
        blank=True,
        null=True,
        default=0,
    )
    title = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=(
            'Select section of the site this page should appear in, '
            'leave blank if this page shouldn\'t appear under any section'))
    slug = AutoSlugField(help_text='This will be the URL for this page',
                         unique=True,
                         overwrite=True,
                         slugify_function=lambda value: value,
                         populate_from=generate_slug)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    # Metadata
    class Meta:
        ordering = ['order', 'created_date']

    # Methods
    def get_absolute_url(self):
        return reverse('page-detail', kwargs={'slug': self.get_slug()})

    # strip tags from slug before returning
    def get_slug(self):
        return self.slug.lstrip('/').rstrip('/')

    # disallow selecting self as parent
    def clean(self):
        if self.parent == self:
            error = "A page can't be its own parent"
            logger.warning(error)
            raise ValidationError(error)

    # display parent hierarchy in admin dropdown list
    def __str__(self):
        hierarchy = []
        self.generate_hierarchy(self, hierarchy)
        title = ' ↣ '.join(hierarchy)
        return title

    def generate_hierarchy(self, instance, hierarchy):
        hierarchy.insert(0, instance.title)
        if instance.parent:
            self.generate_hierarchy(instance.parent, hierarchy)


class Component(models.Model):
    order = models.IntegerField(
        blank=True,
        null=True,
        default=0,
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='components',
    )

    # Metadata
    class Meta:
        ordering = ['order']

    def __str__(self):
        return '#{0}'.format(self.order + 1)


class Editorial(AbstractEditorial):
    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='editorial',
    )


class Embed(AbstractEmbed):
    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='embed',
    )


class Feature(AbstractFeature):

    def get_upload_path(self, filename):
        id = self.component.page_id
        return 'page/{0}/feature/{1}'.format(id, filename)

    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='feature',
    )
    image = models.ImageField(upload_to=get_upload_path, blank=True)


class Image(AbstractImage):

    def get_upload_path(self, filename):
        id = self.component.page_id
        return 'page/{0}/image/{1}'.format(id, filename)

    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='image',
    )
    image = models.ImageField(upload_to=get_upload_path)


class ListItems(AbstractListItems):
    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='list_items',
    )


class ListItem(AbstractListItem):

    def get_upload_path(self, filename):
        id = self.list_items.component.page_id
        return 'page/{0}/list-items/{1}'.format(id, filename)

    image = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        help_text='Image will be cropped and resized to 800x400')
    list_items = models.ForeignKey(
        ListItems,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='list_items',
    )


class Profile(AbstractProfile):
    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='profile',
    )


class ProfileMember(AbstractProfileMember):

    def get_upload_path(self, filename):
        id = self.profile.component.page_id
        return 'page/{0}/profile/{1}'.format(id, filename)

    profile = models.ForeignKey(
        Profile,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='profile_members',
    )
    image = models.ImageField(
        help_text='Image will be cropped and resized to 400x600',
        upload_to=get_upload_path,
        blank=True,
    )


class Quote(AbstractQuote):

    def get_upload_path(self, filename):
        id = self.component.page_id
        return 'page/{0}/quote/{1}'.format(id, filename)

    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='quote',
    )
    image = models.ImageField(upload_to=get_upload_path, blank=True)


class Table(AbstractTable):
    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='table',
    )


class Result(AbstractResult):
    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='result',
    )
    result = models.ForeignKey(
        ResultModel,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='page_result',
    )


class Gallery(AbstractGallery):
    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='gallery',
    )
    gallery = models.ForeignKey(
        GalleryModel,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='page_gallery',
    )
