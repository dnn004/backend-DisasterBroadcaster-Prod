from disaster_broadcaster.models.User import User
from disaster_broadcaster.models.Post import Post
from django.db import models

class Reaction(models.Model):
  REACTION_CHOICES = [
    ('1', 'Like'),
    ('2', 'Sad'),
    ('3', 'Love')
  ]

  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
  reaction = models.CharField(max_length=3, choices=REACTION_CHOICES, default='3')
