from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User, Like
from apps.posts.models import Post
from rest_framework.permissions import IsAuthenticated


class UserList(APIView):
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


class HandleLikes(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk=None):
        """
        Get likes by user or likes by all users, depending on presence of pk
        :param request:
        :param pk:
        :return:
        """
        if pk is not None:
            likes = [(like.post_id, like.user_id) for like in Like.objects.filter(user_id=pk)]
            return Response(likes)
        likes = [(like.post_id, like.user_id) for like in Like.objects.all()]
        return Response(likes)

    def post(self, request, pk):
        """
        Like post by given pk
        :param request:
        :param pk:
        :return:
        """
        try:
            user = request.user
            if user.is_authenticated:
                post = get_object_or_404(Post, id=pk)
                if post.author_id == user.id:
                    return Response({'error': 'user can\'t like own post'})
                like = Like(user=user, post=post)
                like.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response({'error': 'user must be logged in'})
        except Exception as e:
            return Response({'error': str(e)})

    def delete(self, request, pk):
        """
        Unlike post given by pk
        :param request:
        :param pk:
        :return:
        """
        user = request.user
        if user.is_authenticated:
            post = get_object_or_404(Post, id=pk)
            if post.author_id == user.id:
                return Response({'error': 'user can\'t unlike own post'})
            like = get_object_or_404(Like, post=pk, user=user)
            like.delete()
            return Response(status=status.HTTP_200_OK)
        return Response({'error': 'user must be logged in'})


def index(request):
    """
    Every site needs one
    :param request:
    :return:
    """
    return HttpResponse("Welcome to the most awesome social app called Likers.net! All your likes are belong to us!")