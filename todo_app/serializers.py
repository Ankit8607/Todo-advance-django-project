from rest_framework import serializers
from django.contrib.auth.models import User
from todo_app.models import Project, Tag, Task, SubTask


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data["username"],
                password=validated_data["password"],
                email=validated_data["email"],
            )
            return user
        except Exception as e:
            raise serializers.ValidationError(f"Error creating user: {str(e)}")


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ["id", "title", "description", "tags"]

    def create(self, validated_data):
        try:
            tags_data = validated_data.pop("tags", [])
            project = Project.objects.create(**validated_data)
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(
                    owner=self.context["request"].user, **tag_data
                )
                project.tags.add(tag)
            return project
        except Exception as e:
            raise serializers.ValidationError(f"Error creating project: {str(e)}")

    def update(self, instance, validated_data):
        request_user = self.context["request"].user
        if instance.owner != request_user:
            raise serializers.ValidationError(
                "You do not have permission to update this project."
            )
        try:
            tags_data = validated_data.pop("tags", [])
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                
            instance.tags.clear()

            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(
                    owner=self.context["request"].user, **tag_data
                )
                instance.tags.add(tag)

            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError(f"Error updating project: {str(e)}")


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "assigned_to",
            "is_private",
            "tags",
            "is_completed",
        ]

    def create(self, validated_data):
        try:
            tags_data = validated_data.pop("tags", [])
            project = self.context["project"]
            task = Task.objects.create(project=project, **validated_data)
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(
                    owner=self.context["request"].user, **tag_data
                )
                task.tags.add(tag)
            return task
        except Exception as e:
            raise serializers.ValidationError(f"Error creating task: {str(e)}")

    def update(self, instance, validated_data):
        request_user = self.context["request"].user
        if instance.owner != request_user and instance.assigned_to != request_user:
            raise serializers.ValidationError(
                "You do not have permission to update this task."
            )
        try:
            tags_data = validated_data.pop("tags", [])
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if "is_completed" in validated_data:
                if validated_data["is_completed"]:
                    if instance.subtasks.filter(is_completed=False).exists():
                        raise serializers.ValidationError(
                            "Cannot complete task. Some subtasks are not completed."
                        )
                    instance.is_completed = True
                else:
                    instance.is_completed = False

                instance.save()

                if instance.is_completed:
                    instance.check_completion()
                    
            instance.tags.clear()

            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(
                    owner=self.context["request"].user, **tag_data
                )
                instance.tags.add(tag)

            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError(f"Error updating task: {str(e)}")


class SubTaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = SubTask
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "is_private",
            "tags",
            "is_completed",
        ]

    def create(self, validated_data):
        try:
            tags_data = validated_data.pop("tags", [])
            task = self.context["task"]
            subtask = SubTask.objects.create(task=task, **validated_data)
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(
                    owner=self.context["request"].user, **tag_data
                )
                subtask.tags.add(tag)
            return subtask
        except Exception as e:
            raise serializers.ValidationError(f"Error creating subtask: {str(e)}")

    def update(self, instance, validated_data):
        request_user = self.context["request"].user
        if instance.owner != request_user and instance.task.assigned_to != request_user:
            raise serializers.ValidationError(
                "You do not have permission to update this subtask."
            )
        try:
            tags_data = validated_data.pop("tags", [])
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if "is_completed" in validated_data:
                instance.is_completed = validated_data["is_completed"]
                instance.save()
                if instance.is_completed:
                    instance.task.check_completion()

            instance.save()
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(
                    owner=self.context["request"].user, **tag_data
                )
                instance.tags.add(tag)

            return instance
        except Exception as e:
            raise serializers.ValidationError(f"Error updating subtask: {str(e)}")


class PublicProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ["id", "title", "tags"]
