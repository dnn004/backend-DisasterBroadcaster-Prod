from rest_framework import serializers
from disaster_broadcaster.models.Post import Post
from disaster_broadcaster.serializers.User import UserGeneralSerializer
from disaster_broadcaster.serializers.Country import CountryGeneralSerializer

class PostCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = "__all__"

  def create(self, data):
    return Post.objects.create(**data)

class PostGeneralSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = "__all__"

  user_id = UserGeneralSerializer()
  country_id = CountryGeneralSerializer()

class PostUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = "__all__"

  def update(self, instance:Post, data):
    if data.get("country_id"): instance.country_id = data.get("country_id")
    if data.get("media"): instance.media = data.get("media")
    if data.get("content"): instance.content = data.get("content")

    instance.save()
    return instance
