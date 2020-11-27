from django.db import models

class Organization(models.Model):
  name = models.CharField(default='', max_length=200, unique=True)
  address = models.CharField(default='', max_length=200)
  url = models.URLField()
  email = models.EmailField(blank=True, null=True)
