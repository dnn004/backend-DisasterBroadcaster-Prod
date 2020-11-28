from rest_framework import serializers
from disaster_broadcaster.models.Fund import Fund
from disaster_broadcaster.serializers.Disaster import DisasterGeneralSerializer
from disaster_broadcaster.serializers.Organization import OrganizationGeneralSerializer

class FundCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Fund
    fields = '__all__'

  def create(self, data):
    return Fund.objects.create(**data)

class FundGeneralSerializer(serializers.ModelSerializer):
  class Meta:
    model = Fund
    fields = '__all__'

  disaster_id = DisasterGeneralSerializer()
  organization_id = OrganizationGeneralSerializer()

class FundUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Fund
    fields = '__all__'

  def update(self, instance:Fund, data):
    if data.get('disaster_id'): instance.disaster_id = data.get('disaster_id')
    if data.get('organization_id'): instance.organization_id = data.get('organization_id')
    if data.get('fund_page'): instance.fund_page = data.get('fund_page')

    instance.save()
    return instance
