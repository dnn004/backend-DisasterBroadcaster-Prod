import os
from disaster_broadcaster.bucket_delete import s3_delete
from rest_framework import serializers
from disaster_broadcaster.models.Post import Post
from disaster_broadcaster.models.User import User
from disaster_broadcaster.models.Reaction import Reaction
from disaster_broadcaster.models.Comment import Comment
from disaster_broadcaster.serializers.User import UserGeneralSerializer
from disaster_broadcaster.serializers.Country import CountryGeneralSerializer

class PostCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = '__all__'

  def create(self, data):
    return Post.objects.create(**data)

class PostGeneralSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = '__all__'

  user_id = UserGeneralSerializer()
  country_id = CountryGeneralSerializer()

class PostSingleGeneralSerializer(serializers.ModelSerializer):
  comments = serializers.SerializerMethodField()
  like_count = serializers.SerializerMethodField()
  sad_count = serializers.SerializerMethodField()
  love_count = serializers.SerializerMethodField()

  def get_comments(self, instance):
    return_comments = []
    comments = Comment.objects.filter(post_id=instance.id).values('id', 'user_id', 'comment', 'date_created')
    for comment in comments:
      display = {}
      user = User.objects.get(pk=comment.get('user_id'))
      display['id'] = comment.get('id')
      display['username'] = user.username
      display['avatar'] = user.avatar
      display['date_created'] = comment.get('dated_created')
      display['comment'] = comment.get('comment')
      return_comments.append(display)
    return return_comments

  def get_like_count(self, instance):
    return Reaction.objects.filter(post_id=instance.id, reaction=1).count()

  def get_sad_count(self, instance):
    return Reaction.objects.filter(post_id=instance.id, reaction=2).count()

  def get_love_count(self, instance):
    return Reaction.objects.filter(post_id=instance.id, reaction=3).count()

  class Meta:
    model = Post
    fields = '__all__'

  user_id = UserGeneralSerializer()
  country_id = CountryGeneralSerializer()

class PostUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = '__all__'

  def update(self, instance:Post, data):
    if data.get('country_id'): instance.country_id = data.get('country_id')
    if data.get('content'): instance.content = data.get('content')
    if data.get('media'): 
      if os.environ.get('DJANGO_DEBUG') == 'False':
        s3_delete(instance.media.url)
      instance.media = data.get('media')

    instance.save()
    return instance
