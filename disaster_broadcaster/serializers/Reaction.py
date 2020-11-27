from rest_framework import serializers
from disaster_broadcaster.models.Reaction import Reaction
from disaster_broadcaster.serializers.User import UserGeneralSerializer
from disaster_broadcaster.serializers.Post import PostGeneralSerializer

class ReactionCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reaction
    fields = "__all__"

  def create(self, data):
    return Reaction.objects.create(**data)

class ReactionGeneralSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reaction
    fields = "__all__"

  user_id = UserGeneralSerializer()
  post_id = PostGeneralSerializer()

class ReactionUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reaction
    fields = "__all__"

  def update(self, instance:Reaction, data):
    if data.get("reaction"): instance.reaction = data.get("reaction")

    instance.save()
    return instance
