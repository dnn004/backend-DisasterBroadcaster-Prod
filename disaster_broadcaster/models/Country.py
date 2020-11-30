from django.db import models
from django.core.validators import RegexValidator

class Country(models.Model):
  name = models.CharField(max_length=64, unique=True)
  emergency_url = models.URLField(blank=True, null=True)
  phone_regex = RegexValidator(regex=r'^\+?1?\d{1,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
  emergency_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)

  def __str__(self):
    return f"{self.name}"
