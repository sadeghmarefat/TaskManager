from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, CommentViewSet

DefaultRouter = DefaultRouter()
DefaultRouter.register('projects', ProjectViewSet, basename='projects')
DefaultRouter.register('tasks', TaskViewSet, basename='tasks')
DefaultRouter.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(DefaultRouter.urls))
]