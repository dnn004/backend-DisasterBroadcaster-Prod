from disaster_broadcaster.models.Country import Country
from disaster_broadcaster.models.Category import Category
from django.db import models

class Disaster(models.Model):
  country_id = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
  category_id = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
  date_happened = models.DateTimeField(null=True)
