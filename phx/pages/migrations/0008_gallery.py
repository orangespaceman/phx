# Generated by Django 4.1.3 on 2022-11-11 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20191111_1701'),
        ('pages', '0007_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='pages.component')),
                ('gallery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page_gallery', to='gallery.gallery')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
