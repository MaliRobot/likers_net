from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.companies.models import Company
from apps.posts.models import Post

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    company = models.ForeignKey(
        Company,
        null=True,
        on_delete=models.CASCADE,
        related_name='users'
    )


# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ("user", "post")