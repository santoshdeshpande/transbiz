from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel


class State(TimeStampedModel):
    name = models.CharField(max_length=20, unique=True, verbose_name='Name of the State', blank=False)
    short_name = models.CharField(max_length=2, verbose_name='Short Name for the State(KA, MH etc)', blank=False)

    def __unicode__(self):
        return self.name


class City(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True, verbose_name='Name of the city')
    state = models.ForeignKey(State, related_name='cities')

    class Meta:
        verbose_name_plural = 'Cities'
        verbose_name = 'City'

    def __unicode__(self):
        return self.name


class IndustryVertical(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Industry Verticals'
        verbose_name = 'Industry Vertical'

    def __unicode__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    vertical = models.ForeignKey(IndustryVertical)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class SubscriptionPlan(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0, verbose_name='Number of days for this plan')

    class Meta:
        verbose_name_plural = "Subscription Plans"
        verbose_name = "Subscription Plan"

    def __unicode__(self):
        return "%s (%d days) " % (self.name, self.duration)
