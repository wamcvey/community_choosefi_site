#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from itertools import chain

import pytz

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    location = models.TextField(blank=True,
                                help_text="Your approximate address",
                                verbose_name="Address")
    share_location = models.BooleanField(
        default=False,
        help_text="Share location with other members")

    LOCATION_RESOLUTION_CHOICES = [
        (5, "Exact Location"),      # resolution of 11meters, .0001
        (2, "Nearby location (±5km or 3 miles)"),   # .1
        (1, "Neighborhood (±50km or 31 miles"), # 0
        (0, "Region (±500km or 310 miles"),    # 10
    ]
    share_resolution = models.IntegerField(
        default=1,
        choices=LOCATION_RESOLUTION_CHOICES,
        help_text="Amount of resolution to apply to address.")

    local_groups = models.ManyToManyField('choosefi_local.LocalGroupPage')
    topic_groups = models.ManyToManyField('choosefi_local.TopicGroupPage')
    share_group_memberships = models.BooleanField(
        default=False, help_text="Share group membership with other members")
    timezone = models.CharField(
        max_length=128,
        choices=[(x, x) for x in pytz.common_timezones],
        default="UTC",
        help_text="Your Timezone")

    def rounded_location(self, latitude, longitude):
        round_resolution = self.share_resolution -1
        return (round(latitude, round_resolution), round(longitude, round_resolution))


    def upcoming_events(self, limit=20):
        events = []
        for group_page in chain(self.local_groups.all(),
                          self.topic_groups.all()):
            for event in group_page.get_index_children():
                events.append(event)
        # events.sort(key=lambda x: x.most_recent_occurrence())
        return events[:limit]

    def save_test(self, *args, **kwargs):
        # See coderedcms/page_models.CoderedLocationPage.save()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
