from django.db import models
from ckeditor.fields import RichTextField
from ..users.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    lead = models.CharField(max_length=255)
    text = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField()
    language = models.CharField(max_length=3, default='eng')
    date_published = models.DateTimeField('date published', auto_now_add=True)
    date_updated = models.DateTimeField('date updated', null=True, blank=True)

    def __str__(self):
        return self.title