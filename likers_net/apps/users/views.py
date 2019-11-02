from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LikeSerializer
from .models import User, Like
from apps.posts.models import Post
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated


class UserList(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        users = [[user.id, user.username] for user in User.objects.all()]
        return Response(users)

    def post(self, request):
        """
        Register User
        :param request:
        :return:
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        """
        :param pk:
        :return:
        """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        :param request:
        :param pk:
        :param format:
        :return:
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LikeList(generics.ListCreateAPIView):
    model = Like
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def get_queryset(self):
        """
        Get posts by user id and/or post id
        :return:
        """
        queryset = Like.objects.all()
        user = self.request.query_params.get('user')
        post = self.request.query_params.get('post')

        if user:
            queryset = queryset.filter(user_id=user)
        if post:
            queryset = queryset.filter(post_id=post)

        return queryset


class LikeDetail(generics.ListCreateAPIView):
    model = Like
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def post(self, request, pk):
        """
        Like post by given post pk
        :param request:
        :param pk:
        :return:
        """
        try:
            user = request.user
            post = get_object_or_404(Post, id=pk)
            if post.author_id == user.id:
                return Response({'error': 'user can\'t like own post'}, status=status.HTTP_403_FORBIDDEN)
            like = Like(user=user, post=post)
            like.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)})

    def delete(self, request, pk, format=None):
        """
        Unlike post by given post pk
        :param request:
        :param pk:
        :param format:
        :return:
        """
        user = request.user
        post = get_object_or_404(Post, id=pk)
        if post.author_id == user.id:
            return Response({'error': 'user can\'t unlike own post'}, status=status.HTTP_403_FORBIDDEN)
        like = get_object_or_404(Like, post=pk, user=user)
        like.delete()
        return Response(status=status.HTTP_200_OK)


def index(request):
    """
    Every site needs one
    :param request:
    :return:
    """
    return HttpResponse("Welcome to the most awesome social app called Likers.net! All your likes are belong to us!")