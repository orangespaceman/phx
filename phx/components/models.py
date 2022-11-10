from ckeditor.fields import RichTextField
from django.db import models

COMPONENT_TYPES = [
    'editorial',
    'embed',
    'feature',
    'image',
    'list_items',
    'profile',
    'quote',
    'table',
]

ALIGNMENT_CHOICES = (
    ('imageLeft', 'Image left'),
    ('imageRight', 'Image right'),
    ('centre', 'Centre'),
)

EMBED_ALIGNMENT_CHOICES = (
    ('', 'Default'),
    ('responsive', 'Responsive'),
    ('fullSize', 'Full size'),
)

BACKGROUND_CHOICES = (
    ('light', 'Light'),
    ('dark', 'Dark'),
    ('white', 'White'),
)

TEXT_SIZE_CHOICES = (
    ('small', 'Small'),
    ('large', 'Large'),
)


class AbstractComponent(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractEditorial(AbstractComponent):
    title = models.CharField(max_length=200, blank=True)
    content = RichTextField(config_name='text', )

    class Meta:
        abstract = True

    def __str__(self):
        return 'editorial'


class AbstractEmbed(AbstractComponent):
    title = models.CharField(max_length=200, blank=True)
    align = models.CharField(
        choices=EMBED_ALIGNMENT_CHOICES,
        default='',
        blank=True,
        max_length=200,
        help_text="(Leave blank unless you know what you're doing!)",
    )
    content = models.TextField(
        help_text="Careful! Anything you enter here will be embedded "
        "directly in the website...")

    class Meta:
        abstract = True

    def __str__(self):
        return 'embed'


class AbstractFeature(AbstractComponent):
    # add image field directly where used:
    # image = models.ImageField(upload_to=get_upload_path, blank=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    image_alt = models.CharField(max_length=200, blank=True)
    link_url = models.URLField(max_length=200, blank=True)
    link_text = models.CharField(max_length=200, blank=True)
    align = models.CharField(choices=ALIGNMENT_CHOICES, max_length=200)
    background = models.CharField(choices=BACKGROUND_CHOICES, max_length=200)
    text_size = models.CharField(choices=TEXT_SIZE_CHOICES, max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return 'feature'


class AbstractImage(AbstractComponent):
    # add image field directly where used:
    # image = models.ImageField(upload_to=get_upload_path)
    image_alt = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return 'image'


class AbstractListItems(AbstractComponent):

    class Meta:
        abstract = True
        verbose_name = 'list items'
        verbose_name_plural = 'list items'

    def __str__(self):
        return 'list items'


class AbstractListItem(AbstractComponent):
    # add image fields directly where used:
    # image = models.ImageField(upload_to=get_upload_path, blank=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    image_alt = models.CharField(max_length=200, blank=True)
    link_url = models.URLField(max_length=200, blank=True)
    link_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(
        blank=True,
        null=True,
        default=0,
    )

    class Meta:
        abstract = True
        verbose_name = 'list item'
        ordering = ['order', 'id']

    def __str__(self):
        return 'list item'


class AbstractProfile(AbstractComponent):
    title = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return 'profile'


class AbstractProfileMember(AbstractComponent):
    # add image field directly where used:
    # image = models.ImageField(upload_to=get_upload_path, blank=True)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(
        blank=True,
        null=True,
        default=0,
    )

    class Meta:
        abstract = True
        ordering = ['order', 'id']

    def __str__(self):
        return 'profile member'


class AbstractQuote(AbstractComponent):
    # add image field directly where used:
    # image = models.ImageField(upload_to=get_upload_path, blank=True)
    quote = models.TextField()
    author = models.CharField(max_length=200, blank=True)
    image_alt = models.CharField(max_length=200, blank=True)
    align = models.CharField(choices=ALIGNMENT_CHOICES, max_length=200)
    background = models.CharField(choices=BACKGROUND_CHOICES, max_length=200)
    text_size = models.CharField(choices=TEXT_SIZE_CHOICES, max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return 'quote'


class AbstractTable(AbstractComponent):
    title = models.CharField(max_length=200, blank=True)
    content = RichTextField(config_name='table', )

    class Meta:
        abstract = True

    def __str__(self):
        return 'table'
