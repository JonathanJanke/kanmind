from operator import ge

from django.conf.locale import de
from authentication_app.models import User
from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):

    member_count = serializers.IntegerField(read_only=True)
    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_in_progress_count = serializers.IntegerField(read_only=True)
    tasks_done_count = serializers.IntegerField(read_only=True)
    tasks_in_review_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)
    tasks_medium_prio_count = serializers.IntegerField(read_only=True)
    tasks_low_prio_count = serializers.IntegerField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Board.members.field.related_model.objects.all(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_id",
            "members",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_in_progress_count",
            "tasks_done_count",
            "tasks_in_review_count",
            "tasks_high_prio_count",
            "tasks_medium_prio_count",
            "tasks_low_prio_count",
        ]
        read_only_fields = [ "owner_id"]

    def get_response(self):
        def user_data(user):
            return {
                "id": user.id,
                "email": user.email,
                "fullname": user.fullname,
            }

        tasks = self.instance.tasks.prefetch_related("assignees", "reviewers")

        return {
            "id": self.instance.id,
            "title": self.instance.title,
            "owner_id": self.instance.owner_id,
            "members": [
                user_data(member)
                for member in self.instance.members.all()
            ],
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "assignees": [
                        user_data(user) for user in task.assignees.all()
                    ],
                    "reviewers": [
                        user_data(user) for user in task.reviewers.all()
                    ],
                    "due_date": task.due_date,
                    "comments_count": task.comments.count(),
                }
                for task in tasks
            ],
        }