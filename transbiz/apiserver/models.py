from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class State(models.Model):

    name = models.CharField(max_length=20, unique=True, verbose_name='Name of the State')
    short_name = models.CharField(max_length=2, verbose_name='Short Name for the State(KA, MH etc)')

    def __unicode__(self):
        return self.name


