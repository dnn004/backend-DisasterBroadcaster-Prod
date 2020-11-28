from rest_framework import serializers
from disaster_broadcaster.models.Disaster import Disaster
from disaster_broadcaster.serializers.Country import CountryGeneralSerializer
from disaster_broadcaster.serializers.Category import CategoryGeneralSerializer

class DisasterCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Disaster
    fields = '__all__'

  def create(self, data):
    return Disaster.objects.create(**data)

class DisasterGeneralSerializer(serializers.ModelSerializer):
  class Meta:
    model = Disaster
    fields = '__all__'

  country_id = CountryGeneralSerializer()
  category_id = CategoryGeneralSerializer()

class DisasterUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Disaster
    fields = '__all__'

  def update(self, instance:Disaster, data):
    if data.get('country_id'): instance.country_id = data.get('country_id')
    if data.get('category_id'): instance.category_id = data.get('category_id')

    instance.save()
    return instance
