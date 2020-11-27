from rest_framework import serializers
from disaster_broadcaster.models.Country import Country

class CountryCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Country
    fields = "__all__"

  def create(self, data):
    return Country.objects.create(**data)

class CountryGeneralSerializer(serializers.ModelSerializer):
  class Meta:
    model = Country
    fields = "__all__"

class CountryUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Country
    fields = "__all__"

  def update(self, instance:Country, data):
    if data.get("name"): instance.name = data.get("name")
    if data.get("emergency_url"): instance.emergency_url = data.get("emergency_url")
    if data.get("emergency_number"): instance.emergency_number = data.get("emergency_number")
    
    instance.save()
    return instance
