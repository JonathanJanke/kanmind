from rest_framework import serializers

from authentication_app.models import User

from ..models import Comment, Task


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "fullname")
        read_only_fields = fields


STATUS_CHOICES = ("to-do", "in-progress", "review", "done")
PRIORITY_CHOICES = ("low", "medium", "high")


class TaskSerializer(serializers.ModelSerializer):
    board = serializers.IntegerField(source="board_id")
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    priority = serializers.ChoiceField(choices=PRIORITY_CHOICES)
    assignee_id = serializers.PrimaryKeyRelatedField(
        source="assignee",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source="reviewer",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    assignee = UserSummarySerializer(read_only=True)
    reviewer = UserSummarySerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

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
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        )


class SingleTaskSerializer(TaskSerializer):
    class Meta(TaskSerializer.Meta):
        fields = tuple(
            name for name in TaskSerializer.Meta.fields if name not in ("board", "comments_count")
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.fullname", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "created_at", "author", "content")
        read_only_fields = ("id", "created_at", "author")
