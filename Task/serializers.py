from rest_framework import serializers
from .models import Project, Task, Comment
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'status', 'priority', 'due_date', 'created_at', 'updated_at']

    def validate(self, attrs):
        project = attrs.get('project', getattr(self.instance, 'project', None))
        assigned_to = attrs.get('assigned_to', getattr(self.instance, 'assigned_to', None))
        due_date = attrs.get('due_date', getattr(self.instance, 'due_date', None))

        if project and due_date and due_date < project.created_at:
            raise serializers.ValidationError({"due_date": "Due date cannot be before project creation date."})

        if project and assigned_to and assigned_to not in project.members.all():
            raise serializers.ValidationError({"assigned_to": "Assigned user must be a member of the project."})

        return attrs

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['title', 'description', 'owner', 'members', 'tasks', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = ['task', 'author', 'content', 'created_at']