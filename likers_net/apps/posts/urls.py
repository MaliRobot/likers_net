from django.urls import path
from django.conf.urls import url
from . import views
# from rest_framework import routers
from .views import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/posts', PostViewSet)
urlpatterns = router.urls

# urlpatterns = [
#     path('api/posts', views.PostViewSet.as_view({'get': 'list'})),
#     # path('/api/posts/<int:pk>', views.PostDetail.as_view()),
# ]