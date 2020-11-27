from disaster_broadcaster.models.Disaster import Disaster
from disaster_broadcaster.models.Organization import Organization
from django.db import models

class Fund(models.Model):
  disaster_id = models.ForeignKey(Disaster, on_delete=models.CASCADE, blank=True, null=True)
  organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
  fund_page = models.URLField()
  date_created = models.DateTimeField(auto_now_add=True, null=True)
