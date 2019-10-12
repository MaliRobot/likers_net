from django.db import models
from django.conf import settings


# Create your models here.
class Company(models.Model):
    company_id = models.CharField(max_length=64, blank=True)
    company_name = models.CharField(max_length=64, blank=True)
    company_domain = models.TextField(max_length=255, blank=True)


