import os
from disaster_broadcaster.bucket_delete import s3_delete
from rest_framework import serializers
from disaster_broadcaster.models.News import News
from disaster_broadcaster.serializers.Country import CountryGeneralSerializer
from disaster_broadcaster.serializers.Disaster import DisasterGeneralSerializer

class NewsCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = News
    fields = '__all__'

  def create(self, data):
    return News.objects.create(**data)

class NewsGeneralSerializer(serializers.ModelSerializer):
  class Meta:
    model = News
    fields = '__all__'

  country_id = CountryGeneralSerializer()
  disaster_id = DisasterGeneralSerializer()

class NewsUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = News
    fields = '__all__'

  def update(self, instance:News, data):
    if data.get('country_id'): instance.country_id = data.get('country_id')
    if data.get('disaster_id'): instance.disaster_id = data.get('disaster_id')
    if data.get('url'): instance.url = data.get('url')
    if data.get('headline'): instance.headline = data.get('headline')
    if data.get('content'): instance.content = data.get('content')
    if data.get('media'): 
      if os.environ.get('DJANGO_DEBUG') == 'False':
        s3_delete(instance.media.url)
      instance.media = data.get('media')

    instance.save()
    return instance
