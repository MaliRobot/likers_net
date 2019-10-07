from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Welcome to the most awesome social app called Likers.net! All your likes are belong to us!")