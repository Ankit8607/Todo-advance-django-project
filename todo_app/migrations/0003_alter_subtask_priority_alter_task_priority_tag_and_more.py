# Generated by Django 4.2.14 on 2024-07-13 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("todo_app", "0002_alter_project_id_alter_subtask_id_alter_task_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subtask",
            name="priority",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tags",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="project",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="projects", to="todo_app.tag"
            ),
        ),
        migrations.AddField(
            model_name="subtask",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="subtasks", to="todo_app.tag"
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="tasks", to="todo_app.tag"
            ),
        ),
    ]