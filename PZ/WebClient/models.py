from django.db import models
from django.contrib.auth.models import User


class Monitors(models.Model):
    monitor_name = models.CharField(max_length=200)
    monitor_domain = models.URLField()
    user_id = models.ForeignKey(User)

class Hosts(models.Model):
    monitor_id = models.IntegerField()
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
