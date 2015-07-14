from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel


class State(TimeStampedModel):

    name = models.CharField(max_length=20, unique=True, verbose_name='Name of the State')
    short_name = models.CharField(max_length=2, verbose_name='Short Name for the State(KA, MH etc)')

    def __unicode__(self):
        return self.name


class IndustryVertical(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

