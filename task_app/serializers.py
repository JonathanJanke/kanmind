from .models import Task
from authentication_app.models import User

from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate(self, data):

        assignee = User.objects.filter(pk=data.get("assignee_id")).first()
        reviewer = User.objects.filter(pk=data.get("reviewer_id")).first()
        request = self.context.get("request")
        user = request.user

        board = data.get("board")
        if board and not (board.owner_id == user.id or user in board.members.all()):
            raise serializers.ValidationError("You do not have permission to create a task for this board.")
        if board and not (board.owner_id == assignee or reviewer or assignee or reviewer in board.members.all()):
            raise serializers.ValidationError("That´s not a boardmember")
        
        if data.get("status") not in ["to-do", "in-progress", "review", "done"]:
            raise serializers.ValidationError("Invalid status value.")
        if data.get("priority") not in ["low", "medium", "high"]:
            raise serializers.ValidationError("Invalid priority value.")

        return data
        
    def get_response(self, obj):

        assignee = User.objects.filter(pk=obj.assignee_id).first()
        reviewer = User.objects.filter(pk=obj.reviewer_id).first()

        return {
            "id": obj.id,
            "board": obj.board.id,
            "title": obj.title,
            "description": obj.description,
            "status": obj.status,
            "priority": obj.priority,
            "assignee": {"id": assignee.id, "email": assignee.email, "fullname": assignee.fullname} if assignee else None,
            "reviewer": {"id": reviewer.id, "email": reviewer.email, "fullname": reviewer.fullname} if reviewer else None,
            "due_date": obj.due_date,
            # "comments_count": obj.comments.count(),
        }