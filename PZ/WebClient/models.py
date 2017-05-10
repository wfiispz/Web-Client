from django.db import models
from django.contrib.auth.models import User


class Monitors(models.Model):
    monitor_name = models.CharField(max_length=200)
    monitor_domain = models.URLField()
    user_id = models.ForeignKey(User)


class Page(models.Model):
    size = models.IntegerField()
    number = models.IntegerField()
    total_count = models.IntegerField()


class Measurements(models.Model):
    host = models.URLField()
    metric = models.CharField(max_length=10)
    unit = models.CharField(max_length=1)
    max_value = models.IntegerField()
    complex_mes = models.BooleanField()
    values = models.URLField()


class Values(models.Model):
    value = models.IntegerField()
    datetime = models.DateTimeField()


class Resources(models.Model):
    id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    measurements = models.TextField(null=True)
