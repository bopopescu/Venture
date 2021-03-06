# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.db import models
from django.contrib.auth.models import User
from djangocms_text_ckeditor import fields
from filer.fields.image import FilerImageField
from newsletter_subscription.models import SubscriptionBase
from django.conf import settings
from venturelift_cms.tasks import send_notification

AUDIOVISUALCHOICES = (
    ("Podcast", "Podcast"),
    ("Video", "Video"),
)


class Category(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Media category'
        verbose_name_plural = 'Media categories'


class TextMedia(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True)
    author = models.ForeignKey(User)
    body = fields.HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    thumbnail_image = models.FileField(upload_to='pic_folder/',null=True)
    priority = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Media article'
        verbose_name_plural = 'Articles media'


class AudioVisual(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    path = models.TextField()
    author = models.ForeignKey(User)
    vla_tv = models.BooleanField(default=False, help_text='This media is property of VLA')
    category = models.CharField(max_length=100, choices=AUDIOVISUALCHOICES)
    sub_category = models.ForeignKey(Category, null=True)
    priority = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Audio/visual media'
        verbose_name_plural = 'Audio/visual media'


class Subscription(SubscriptionBase):

    class Meta:
        verbose_name = 'Newsletter subscriber'
        verbose_name_plural = 'Newsletter subscribers'

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    title = models.CharField(max_length=250)
    body = fields.HTMLField()
    recipients = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        subs = Subscription.objects.filter(is_active=True)
        emails = [sub.email for sub in subs]
        self.recipients = json.dumps(emails)

        send_notification.delay(self.title, self.body,
                                settings.EMAIL_HOST_USER, emails)
        super(Newsletter, self).save(*args, **kwargs)
