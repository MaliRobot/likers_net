from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/users', views.UserCreate.as_view(), name='user-create'),
]