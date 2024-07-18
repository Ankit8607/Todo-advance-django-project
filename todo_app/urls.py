from django.urls import path
from todo_app.views import (
    TagViewSet,
    UserViewSet,
    ProjectViewSet,
    TaskViewSet,
    SubTaskViewSet,
    PublicProjectViewSet,
)

urlpatterns = [
    path(
        "users/",
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="user-list-create",
    ),
    path(
        "projects/",
        ProjectViewSet.as_view({"get": "list", "post": "create"}),
        name="project-list-create",
    ),
    path(
        "projects/<uuid:pk>/",
        ProjectViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
            }
        ),
        name="project-detail",
    ),
    path(
        "projects/<uuid:project>/tasks/",
        TaskViewSet.as_view({"get": "list", "post": "create"}),
        name="task-list-create",
    ),
    path(
        "projects/<uuid:project>/tasks/<uuid:pk>/",
        TaskViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
            }
        ),
        name="task-detail",
    ),
    path(
        "tasks/<uuid:task>/subtasks/",
        SubTaskViewSet.as_view({"get": "list", "post": "create"}),
        name="subtask-list-create",
    ),
    path(
        "tasks/<uuid:task>/subtasks/<uuid:pk>/",
        SubTaskViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
            }
        ),
        name="subtask-detail",
    ),
    path(
        "tags/",
        TagViewSet.as_view({"get": "list", "post": "create"}),
        name="tag-list-create",
    ),
    path(
        "tags/<uuid:pk>/",
        TagViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
            }
        ),
        name="tag-detail",
    ),
    path(
        "public-projects/",
        PublicProjectViewSet.as_view(
            {
                "get": "list",
            }
        ),
        name="public-project-detail",
    ),
]
