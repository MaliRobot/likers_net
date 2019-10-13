from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.companies.models import Company
from apps.posts.models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver
import clearbit
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    company = models.ForeignKey(
        Company,
        null=True,
        on_delete=models.CASCADE,
        related_name='users'
    )


@receiver(post_save, sender=User)
def create_user_company(sender, instance, created, **kwargs):
    """
    Create company from given user's email
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if settings.DEBUG == 0:
        clearbit.key = settings.CLEARBIT_KEY
        response = clearbit.Enrichment.find(email=instance.email, stream=True)
        if response['company'] is not None:
            company_id = response['company']['id']
            company_name = response['company']['name']
            company_domain = response['company']['domain']
            if created:
                Company.objects.create(
                    company_id=company_id,
                    company_name=company_name,
                    company_domain=company_domain,
                )



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")