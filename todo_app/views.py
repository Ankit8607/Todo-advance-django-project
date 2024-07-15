from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from todo_app.models import Project, Task, SubTask
from todo_app.serializers import (
    ProjectSerializer,
    PublicProjectSerializer,
    TagSerializer,
    TaskSerializer,
    SubTaskSerializer,
    UserSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.db import models
from rest_framework.exceptions import PermissionDenied


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.request.user.tags.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "tags__name"]

    def get_queryset(self):
        return self.request.user.projects.prefetch_related("tags")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description", "tags__name", "due_date"]

    def get_queryset(self):
        project_id = self.kwargs.get("project")
        return (
            Task.objects.filter(
                models.Q(owner=self.request.user)
                | models.Q(assigned_to=self.request.user)
                | models.Q(is_private=False),
                project=project_id,
            )
            .select_related("project", "assigned_to")
            .prefetch_related("tags")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        project_id = self.kwargs.get("project")
        project = Project.objects.get(id=project_id)
        context["project"] = project
        return context

    def perform_create(self, serializer):
        project = serializer.context["project"]
        if project.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission as you are not projecr owner"
            )

        task = serializer.save(owner=self.request.user)
        if task.is_private:
            task.subtasks.update(is_private=True)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class SubTaskViewSet(viewsets.ModelViewSet):

    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description", "tags__name", "due_date"]

    def get_queryset(self):
        task_id = self.kwargs.get("task")
        return (
            SubTask.objects.filter(
                models.Q(owner=self.request.user)
                | models.Q(task__assigned_to=self.request.user)
                | models.Q(is_private=False),
                task=task_id,
            )
            .select_related("task")
            .prefetch_related("tags")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        task_id = self.kwargs.get("task")
        task = Task.objects.get(id=task_id)
        context["task"] = task
        return context

    def perform_create(self, serializer):
        task = serializer.context["task"]
        if task.owner != self.request.user and task.assigned_to != self.request.user:
            raise PermissionDenied(
                "You do not have permission as you are not task owner or task assignee"
            )
        subtask = serializer.save(owner=self.request.user)
        if subtask.is_private:
            subtask.task.is_private = True
            subtask.task.save()


class PublicProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = PublicProjectSerializer
    permission_classes = [permissions.AllowAny]
