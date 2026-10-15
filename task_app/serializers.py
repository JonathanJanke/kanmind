from django.http import request

from .models import Comment, Task
from authentication_app.models import User

from rest_framework import serializers


class UserIdListField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        values = data if isinstance(data, list) else [data]
        result = []
        for value in values:
            result.append(super().to_internal_value(value))
        return result

def validate_board_user(self, data):
    """Prüft, ob alle Assignees/Reviewer zum Board gehören."""

    board = data.get("board")
    if board is None and self.instance is not None:
        board = self.instance.board

    for relation_name, request_field in (
        ("assignees", "assignee_id"),
        ("reviewers", "reviewer_id"),
    ):
        users = data.get(relation_name)
        if users is None and self.instance is not None:
            users = getattr(self.instance, relation_name).all()
        if users is None:
            continue
        if not isinstance(users, (list, tuple, set)):
            users = [users]
        if board:
            for user in users:
                if board.owner_id != user.id and not board.members.filter(pk=user.id).exists():
                    raise serializers.ValidationError({
                        request_field: "A user is not a board member."
                    })

    return data


class TaskSerializer(serializers.ModelSerializer):
    assignee_id = UserIdListField(
        source="assignees",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
    )
    reviewer_id = UserIdListField(
        source="reviewers",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee_id",
            "reviewer_id",
            "due_date",
        )

    def validate(self, data):
        """Validiert die Task-Daten einschließlich der Board-Zugehörigkeit des Assignees."""
        validate_board_user(self, data)
        return data
        
    def get_response(self, obj):
        """Erstellt die API-Darstellung eines Tasks samt Assignees und Reviewern."""

        return {
            "id": obj.id,
            "board": obj.board.id,
            "title": obj.title,
            "description": obj.description,
            "status": obj.status,
            "priority": obj.priority,
            "assignees": [
                {"id": user.id, "email": user.email, "fullname": user.fullname}
                for user in obj.assignees.all()
            ],
            "reviewers": [
                {"id": user.id, "email": user.email, "fullname": user.fullname}
                for user in obj.reviewers.all()
            ],
            "due_date": obj.due_date,
            "comments_count": obj.comments.count(),
        }

class SingleTaskSerializer(serializers.ModelSerializer):
    assignee_id = UserIdListField(
        source="assignees",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
    )
    reviewer_id = UserIdListField(
        source="reviewers",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee_id",
            "reviewer_id",
            "due_date",
        )

    def validate(self, data): 
        """Validiert die Task-Daten einschließlich der Board-Zugehörigkeit des Assignees."""
        validate_board_user(self, data)
        return data

    def get_response(self, obj):
        """Erstellt die API-Darstellung eines einzelnen Tasks samt Benutzerdetails."""

        return {
            "id": obj.id,
            "board": obj.board.id,
            "title": obj.title,
            "description": obj.description,
            "status": obj.status,
            "priority": obj.priority,
            "assignees": [
                {"id": user.id, "email": user.email, "fullname": user.fullname}
                for user in obj.assignees.all()
            ],
            "reviewers": [
                {"id": user.id, "email": user.email, "fullname": user.fullname}
                for user in obj.reviewers.all()
            ],
            "due_date": obj.due_date,
            "comments_count": obj.comments.count(),
        }

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]

    def validate(self, data):
        """Prüft, ob der Ziel-Task existiert und der Kommentartext gesetzt ist."""
        task_id = self.context.get("task_id")
        if task_id is None or not Task.objects.filter(pk=task_id).exists():
            raise serializers.ValidationError({
                "task_id": "Task not found."
            })
        if not data.get("content"):
            raise serializers.ValidationError({
                "content": "Content is required."
            })
        return data

    def get_response(self, obj):
        """Erstellt die API-Darstellung eines Kommentars einschließlich Autor und Erstellungszeit."""
        return {
            "id": obj.id,
            "created_at": obj.created_at,
            "author": obj.author.fullname,
            "content": obj.content,
        }
