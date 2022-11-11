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
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from gallery.models import Gallery as GalleryModel
from results.models import Result as ResultModel


class News(models.Model):
    """ News articles """

    # Fields
    title = models.CharField(max_length=200)
    slug = AutoSlugField(
        populate_from='title',
        help_text='This is used as the URL for this news item',
        unique=False,
        max_length=200)
    summary = models.TextField(
        max_length=1000,
        help_text='Text used on the news listing page',
    )
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
        verbose_name = 'news article'
        verbose_name_plural = 'news articles'
        ordering = ['-created_date']

    # Methods
    def get_absolute_url(self):
        return reverse('news-detail',
                       kwargs={
                           'pk': self.id,
                           'slug': self.slug,
                       })

    def __str__(self):
        return self.title


class Thumbnail(models.Model):

    def get_upload_path(self, filename):
        id = self.news_id
        return 'news/{0}/thumbnail/{1}'.format(id, filename)

    news = models.OneToOneField(
        News,
        on_delete=models.CASCADE,
        related_name='thumbnail',
    )
    image = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        help_text=(
            'Image to display on the news listing page, '
            'it will be cropped and resized to 700x500 if it isn\'t already'))
    image_alt = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.news.title


class Component(models.Model):
    order = models.IntegerField(
        blank=True,
        null=True,
        default=0,
    )
    news = models.ForeignKey(
        News,
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
        id = self.component.news_id
        return 'news/{0}/feature/{1}'.format(id, filename)

    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='feature',
    )
    image = models.ImageField(upload_to=get_upload_path, blank=True)


class Image(AbstractImage):

    def get_upload_path(self, filename):
        id = self.component.news_id
        return 'news/{0}/image/{1}'.format(id, filename)

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
        id = self.list_items.component.news_id
        return 'news/{0}/list-items/{1}'.format(id, filename)

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
        id = self.profile.component.news_id
        return 'news/{0}/profile/{1}'.format(id, filename)

    profile = models.ForeignKey(
        Profile,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='profile_members',
    )
    image = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        help_text='Image will be cropped and resized to 400x600',
    )


class Quote(AbstractQuote):

    def get_upload_path(self, filename):
        id = self.component.news_id
        return 'news/{0}/quote/{1}'.format(id, filename)

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
        related_name='news_result',
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
        related_name='news_gallery',
    )
