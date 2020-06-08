# Generated by Django 2.2.12 on 2020-06-07 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choosefi_local', '0008_topic_groups'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='local_groups',
            field=models.ManyToManyField(to='choosefi_local.LocalGroupPage'),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.TextField(blank=True, help_text='Your approximate address', verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='user',
            name='share_location',
            field=models.BooleanField(default=False, help_text='Share location with other members'),
        ),
        migrations.AddField(
            model_name='user',
            name='share_resolution',
            field=models.IntegerField(default=0, help_text='Amount of resolution to apply to address. 0=exact. 5=appx 100km/60miles'),
        ),
        migrations.AddField(
            model_name='user',
            name='topic_groups',
            field=models.ManyToManyField(to='choosefi_local.TopicGroupPage'),
        ),
    ]