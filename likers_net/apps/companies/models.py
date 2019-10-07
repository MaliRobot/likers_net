from django.db import models
from ..users.models import User

# Create your models here.
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_id = models.CharField(max_length=64, blank=True)
    company_name = models.CharField(max_length=64, blank=True)
    company_domain = models.TextField(max_length=255, blank=True)