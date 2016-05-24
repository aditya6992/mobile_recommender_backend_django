from __future__ import unicode_literals

from django.db import models

# Create your models here.

# class phone(models.Model):
#     url = models.charField()
#     name = models.charField()
#     camera = models.FloatField()
#     ram = models.IntegerField()
#     memory = models.IntegerField()
#     battery = models.IntegerField()
#
#     def __str__(self):
#         return self.name

class Mobile(object):
    def __init__(self, url, name, camera, ram, storage, battery):
        self.url = url
        self.name = name
        self.camera = camera
        self.ram = ram
        self.storage = storage
        self.battery = battery
