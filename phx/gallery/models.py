from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.formats import date_format
from django_extensions.db.fields import AutoSlugField


class Gallery(models.Model):
    """ Gallery """

    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title',
                         help_text='This is used as the URL for this gallery',
                         unique=False,
                         max_length=200)
    summary = models.TextField(
        max_length=1000,
        help_text='Text used on the gallery listing page',
        blank=True,
    )
    event_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'gallery'
        verbose_name_plural = 'gallery'
        ordering = ['-created_date']

    def get_absolute_url(self):
        return reverse('gallery-detail',
                       kwargs={
                           'pk': self.id,
                           'slug': self.slug,
                       })

    def __str__(self):
        return '{} ({})'.format(self.title,
                                date_format(self.created_date, "D j M Y"))


class Thumbnail(models.Model):

    def get_upload_path(self, filename):
        id = self.gallery_id
        return 'gallery/{0}/thumbnail/{1}'.format(id, filename)

    gallery = models.OneToOneField(
        Gallery,
        on_delete=models.CASCADE,
        related_name='thumbnail',
    )
    image = models.ImageField(
        upload_to=get_upload_path,
        help_text=(
            'Image to display on the gallery listing page, '
            'it will be cropped and resized to 700x500 if it isn\'t already'))
    image_alt = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.gallery.title


class Image(models.Model):

    def get_upload_path(self, filename):
        id = self.gallery_id
        return 'gallery/{0}/image/{1}'.format(id, filename)

    image_alt = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to=get_upload_path)
    order = models.PositiveIntegerField(default=1)
    gallery = models.ForeignKey(
        Gallery,
        on_delete=models.CASCADE,
        related_name='images',
    )

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.caption
