from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):

    member_count = serializers.IntegerField(read_only=True)
    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)
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
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
            "members",
        ]
        read_only_fields = [ "owner_id"]