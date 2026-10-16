from operator import ge

from django.conf.locale import de
from authentication_app.models import User
from rest_framework import serializers
from ..models import Board


def user_data(user):
    return {
        "id": user.id,
        "email": user.email,
        "fullname": user.fullname,
    }


class UserPrimaryKeyListField(serializers.ListField):
    child = serializers.IntegerField()

    def to_internal_value(self, data):
        pks = super().to_internal_value(data)
        users_by_pk = User.objects.in_bulk(set(pks))
        for pk in pks:
            if pk not in users_by_pk:
                raise serializers.ValidationError(
                    f'Invalid pk "{pk}" - object does not exist.'
                )
        return [users_by_pk[pk] for pk in pks]


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
    members = UserPrimaryKeyListField(write_only=True, required=False)

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
        board = self.instance
        return {
            "id": board.id,
            "title": board.title,
            "member_count": board.member_count,
            "ticket_count": board.ticket_count,
            "tasks_to_do_count": board.tasks_to_do_count,
            "tasks_high_prio_count": board.tasks_high_prio_count,
            "owner_id": board.owner_id,
        }

    def get_update_response(self):
        board = self.instance
        owner = User.objects.filter(pk=board.owner_id).first()
        return {
            "id": board.id,
            "title": board.title,
            "owner_data": user_data(owner) if owner else None,
            "members_data": [user_data(m) for m in board.members.all()],
        }

    def get_detail_response(self):
        board = self.instance
        return {
            "id": board.id,
            "title": board.title,
            "owner_id": board.owner_id,
            "members": [user_data(m) for m in board.members.all()],
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "assignee": user_data(task.assignee) if task.assignee else None,
                    "reviewer": user_data(task.reviewer) if task.reviewer else None,
                    "due_date": task.due_date,
                    "comments_count": task.comments_count,
                }
                for task in board.tasks.all()
            ],
        }