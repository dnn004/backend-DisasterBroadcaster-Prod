from rest_framework import serializers
from disaster_broadcaster.models.Comment import Comment
from disaster_broadcaster.serializers.User import UserGeneralSerializer
from disaster_broadcaster.serializers.Post import PostGeneralSerializer

class CommentCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'

  def create(self, data):
    return Comment.objects.create(**data)

class CommentGeneralSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'

  user_id = UserGeneralSerializer()
  post_id = PostGeneralSerializer()

class CommentUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'

  def update(self, instance:Comment, data):
    if data.get('comment'): instance.comment = data.get('comment')

    instance.save()
    return instance
