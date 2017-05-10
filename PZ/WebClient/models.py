from django.db import models
from django.contrib.auth.models import User


class Monitors(models.Model):
    monitor_name = models.CharField(max_length=200)
    monitor_domain = models.URLField()
    user_id = models.ForeignKey(User)


class Page(models.Model):
    size = models.IntegerField()
    number = models.IntegerField()
    totalCount = models.IntegerField()


class Measurements(models.Model):
    host = models.URLField()
    metric = models.CharField(max_length=10)
    unit = models.CharField(max_length=1)
    maxValue = models.IntegerField()
    complex = models.BooleanField()
    values = models.URLField()


class Values(models.Model):
    value = models.IntegerField()
    datetime = models.DateTimeField()

class Resources(models.Model):
    id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    measurements = models.TextField(null=Trued)


# class MyJson(models.Model):
#
#     def __init__(self, resources, page):
#         """Init method"""
#         self.resources = resources
#         self.page = page
#
#     def to_json(self):
#         """Serializes object to JSON"""
#         return json.dumps(self, default=lambda myjson: myjson.__dict__, sort_keys=False, indent=4)
