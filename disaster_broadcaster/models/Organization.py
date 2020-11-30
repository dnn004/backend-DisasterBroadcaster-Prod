from django.db import models
import os
from disaster_broadcaster.filepaths.FilePath import FilePath
from disaster_broadcaster.bucket_delete import s3_delete

class Organization(models.Model):
  name = models.CharField(default='', max_length=200, unique=True)
  address = models.CharField(default='', max_length=200)
  url = models.URLField()
  email = models.EmailField(blank=True, null=True)
  logo = models.FileField(upload_to=FilePath.logo, null=True)

  def __str__(self):
    return f"{self.name}"

  # Override save
  def save(self, *args, **kwargs):
    if self.pk is None:
      saved_logo = self.logo
      self.logo = None
      super(Organization, self).save(*args, **kwargs)
      self.logo = saved_logo
      super(Organization, self).save()
    else:
      super(Organization, self).save()
