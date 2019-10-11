from django.urls import path
from django.conf.urls import url
from . import views
# from rest_framework import routers
from .views import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/posts', PostViewSet)
urlpatterns = router.urls
