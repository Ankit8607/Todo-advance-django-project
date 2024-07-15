from django.db import models
import uuid
from django.contrib.auth.models import User


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name="tags", on_delete=models.CASCADE)


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        User,
        related_name="assigned_tasks",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    is_private = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)
    is_completed = models.BooleanField(default=False) 

    def check_completion(self):
        if self.subtasks.filter(is_completed=False).exists():
            return False
        self.is_completed = True
        self.save()
        return True


class SubTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name="subtasks", on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="subtasks", blank=True)
    is_completed = models.BooleanField(default=False) 
