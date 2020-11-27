from django.db import models

class Category(models.Model):
  name = models.CharField(max_length=120)
  guide_url = models.URLField()
  description = models.TextField()
