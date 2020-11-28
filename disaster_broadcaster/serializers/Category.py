from rest_framework import serializers
from disaster_broadcaster.models.Category import Category
from disaster_broadcaster.serializers.Country import CountryGeneralSerializer

class CategoryCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'

  def create(self, data):
    return Category.objects.create(**data)

class CategoryGeneralSerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'

class CategoryUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'

  def update(self, instance:Category, data):
    if data.get('name'): instance.name = data.get('name')
    if data.get('guide_url'): instance.guide_url = data.get('guide_url')
    if data.get('description'): instance.description = data.get('description')

    instance.save()
    return instance
