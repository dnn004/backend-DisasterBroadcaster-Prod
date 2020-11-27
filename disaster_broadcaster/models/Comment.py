from disaster_broadcaster.models.User import User
from disaster_broadcaster.models.Post import Post
from django.db import models

class Comment(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
  comment = models.CharField(max_length=1024, blank=True, default=None)
  date_created = models.DateTimeField(auto_now_add=True, null=True)
