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
    share_location = models.BooleanField(default=False,
                                         help_text="Share location with other members")
    share_resolution = models.IntegerField(
        default=0,
        help_text="Amount of resolution to apply to address. 0=exact. 5=appx 100km/60miles")

    local_groups = models.ManyToManyField('choosefi_local.LocalGroupPage')
    topic_groups = models.ManyToManyField('choosefi_local.TopicGroupPage')
    share_group_memberships = models.BooleanField(
        default=False, help_text="Share group membership with other members")
    timezone = models.CharField(
        max_length=128,
        choices=[(x, x) for x in pytz.common_timezones],
        default="UTC",
        help_text="Your Timezone")


    def upcoming_events(self, limit=20):
        events = []
        for page in chain(self.local_groups.all(),
                          self.topic_groups.all()):
            for event in page.upcoming_events():
                event['page'] = page
                events.append(event)
        events.sort(key=lambda x: x['start'])
        return events[:limit]

    def save_test(self, *args, **kwargs):
        # See coderedcms/page_models.CoderedLocationPage.save()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
