import os
from disaster_broadcaster.filepaths.FilePath import FilePath
from disaster_broadcaster.bucket_delete import s3_delete
from disaster_broadcaster.models.User import User
from disaster_broadcaster.models.Country import Country
from django.db import models


class Post(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
  content = models.CharField(max_length=1024, blank=True, default=None)
  media = models.FileField(upload_to=FilePath.post_upload, null=True)
  date_created = models.DateTimeField(auto_now_add=True, null=True)

  # Override save
  def save(self, *args, **kwargs):
    if self.pk is None:
      saved_media = self.media
      self.media = None
      super(Post, self).save(*args, **kwargs)
      self.media = saved_media
      super(Post, self).save()
    else:
      # Delete old media from S3
      if os.environ.get('DJANGO_DEBUG') == 'False':
        s3_delete('media/post/' + str(self.pk) + "/" + str(self.media))
      super(Post, self).save()
