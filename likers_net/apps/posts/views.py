from django.http import HttpResponse, Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
from .serializers import PostSerializer
from .models import Post
from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('title')


