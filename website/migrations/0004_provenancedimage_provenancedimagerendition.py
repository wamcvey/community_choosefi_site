# Generated by Django 2.2.12 on 2020-06-26 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import wagtail.core.models
import wagtail.images.models
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('website', '0003_auto_20200609_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProvenancedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.images.models.get_upload_to, verbose_name='file', width_field='width')),
                ('width', models.IntegerField(editable=False, verbose_name='width')),
                ('height', models.IntegerField(editable=False, verbose_name='height')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('focal_point_x', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_y', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_width', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_height', models.PositiveIntegerField(blank=True, null=True)),
                ('file_size', models.PositiveIntegerField(editable=False, null=True)),
                ('file_hash', models.CharField(blank=True, editable=False, max_length=40)),
                ('image_attribution', models.CharField(blank=True, help_text='Who is the source of the image', max_length=1024)),
                ('image_attribution_url', models.URLField(blank=True, help_text='URL to the origination of the image', max_length=1024)),
                ('show_attribution', models.BooleanField(default=False, help_text='Source of the image requests the display of the attribution')),
                ('license_notes', models.TextField(blank=True, help_text='Any extra info on image license (not to be displayed)')),
                ('collection', models.ForeignKey(default=wagtail.core.models.get_root_collection_id, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Collection', verbose_name='collection')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags')),
                ('uploaded_by_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by user')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='ProvenancedImageRendition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_spec', models.CharField(db_index=True, max_length=255)),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.images.models.get_rendition_upload_to, width_field='width')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(blank=True, default='', editable=False, max_length=16)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renditions', to='website.ProvenancedImage')),
            ],
            options={
                'unique_together': {('image', 'filter_spec', 'focal_point_key')},
            },
        ),
    ]