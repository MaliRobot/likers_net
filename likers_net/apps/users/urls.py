from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/users', views.UserList.as_view()),
    path('api/users/<int:pk>', views.UserDetail.as_view()),
    # path('api/users/<int:pk>', views.UserDetail.as_view()),
    path('api/likes/', views.HandleLikes.as_view()),
    path('api/likes/<int:pk>', views.HandleLikes.as_view()),
]