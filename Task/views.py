from django.shortcuts import render
from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework import viewsets
from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer

class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return obj.owner == request.user or request.user in obj.members.all()
        elif isinstance(obj, Task):
            return obj.project.owner == request.user or request.user in obj.project.members.all()
        elif isinstance(obj, Comment):
            return obj.task.project.owner == request.user or request.user in obj.task.project.members.all()
        return False


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrMember]

    def get_queryset(self):
        return self.queryset.filter(Q(owner=self.request.user) | Q(members__in=[self.request.user]))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrMember]

    def get_queryset(self):
        return self.queryset.select_related('project', 'assigned_to').filter(Q(owner=self.request.user) | Q(members__in=[self.request.user]))

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrMember]

    def get_queryset(self):
        return self.queryset.select_related('task', 'task__project', 'task__assigned_to').filter(Q(owner=self.request.user) | Q(members__in=[self.request.user]))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
