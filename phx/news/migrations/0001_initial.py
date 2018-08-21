# Generated by Django 2.1 on 2018-08-21 07:55

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import news.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('content', ckeditor.fields.RichTextField()),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='editorial', to='news.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Embed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('content', models.TextField(help_text='Careful! Anything you enter here will be embedded directly in the website...')),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='embed', to='news.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, max_length=200)),
                ('content', models.TextField()),
                ('image_alt', models.CharField(blank=True, max_length=200)),
                ('link_url', models.URLField(blank=True)),
                ('link_text', models.CharField(blank=True, max_length=200)),
                ('align', models.CharField(choices=[('imageLeft', 'Image left'), ('imageRight', 'Image right'), ('centre', 'Centre')], max_length=200)),
                ('background', models.CharField(choices=[('light', 'Light'), ('dark', 'Dark'), ('white', 'White')], max_length=200)),
                ('image', models.ImageField(blank=True, upload_to=news.models.Feature.get_upload_path)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='feature', to='news.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('image_alt', models.CharField(blank=True, max_length=200)),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(upload_to=news.models.Image.get_upload_path)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='news.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('content', models.TextField(blank=True)),
                ('image_alt', models.CharField(blank=True, max_length=200)),
                ('link_url', models.URLField(blank=True)),
                ('link_text', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(blank=True, help_text='Image will be cropped and resized to 800x400', upload_to=news.models.ListItem.get_upload_path)),
            ],
            options={
                'verbose_name': 'list item',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ListItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='list_items', to='news.Component')),
            ],
            options={
                'verbose_name': 'list items',
                'verbose_name_plural': 'list items',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, help_text='This is used as the URL for this news item', max_length=200, populate_from='title')),
                ('summary', models.TextField(help_text='Text used on the news listing page', max_length=1000)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'news article',
                'verbose_name_plural': 'news articles',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='news.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfileMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, help_text='Image will be cropped and resized to 400x600', upload_to=news.models.ProfileMember.get_upload_path)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_members', to='news.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('quote', models.TextField()),
                ('author', models.CharField(blank=True, max_length=200)),
                ('image_alt', models.CharField(blank=True, max_length=200)),
                ('align', models.CharField(choices=[('imageLeft', 'Image left'), ('imageRight', 'Image right'), ('centre', 'Centre')], max_length=200)),
                ('background', models.CharField(choices=[('light', 'Light'), ('dark', 'Dark'), ('white', 'White')], max_length=200)),
                ('image', models.ImageField(blank=True, upload_to=news.models.Quote.get_upload_path)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quote', to='news.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('content', ckeditor.fields.RichTextField()),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='table', to='news.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text="Image to display on the news listing page, it will be cropped and resized to 700x500 if it isn't already", upload_to=news.models.Thumbnail.get_upload_path)),
                ('image_alt', models.CharField(blank=True, max_length=200)),
                ('news', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='thumbnail', to='news.News')),
            ],
        ),
        migrations.AddField(
            model_name='listitem',
            name='list_items',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='list_items', to='news.ListItems'),
        ),
        migrations.AddField(
            model_name='component',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='news.News'),
        ),
    ]
