from django.http import HttpResponse, Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PostSerializer
from .models import Post
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class PostViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('title')
    filterset_fields = ['author']
