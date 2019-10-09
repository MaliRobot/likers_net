from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer


class UserCreate(APIView):
    """
    Creates the user.
    """
    def post(self, request, format='json'):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
def index(request):
    return HttpResponse("Welcome to the most awesome social app called Likers.net! All your likes are belong to us!")