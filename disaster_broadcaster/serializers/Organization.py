import os
from disaster_broadcaster.bucket_delete import s3_delete
from rest_framework import serializers
from disaster_broadcaster.models.Organization import Organization

class OrganizationCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Organization
    fields = '__all__'

  def create(self, data):
    return Organization.objects.create(**data)

class OrganizationGeneralSerializer(serializers.ModelSerializer):
  class Meta:
    model = Organization
    fields = '__all__'

class OrganizationUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Organization
    fields = '__all__'

  def update(self, instance:Organization, data):
    if data.get('name'): instance.name = data.get('name')
    if data.get('address'): instance.address = data.get('address')
    if data.get('url'): instance.url = data.get('url')
    if data.get('email'): instance.email = data.get('email')
    if data.get('logo'): 
      if os.environ.get('DJANGO_DEBUG') == 'False':
        s3_delete(instance.logo.url)
      instance.logo = data.get('logo')

    instance.save()
    return instance
