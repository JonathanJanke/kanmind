from django.http import request

from .models import Comment, Task
from authentication_app.models import User

from rest_framework import serializers

def validate_board_user(self, data):
    """Prüft, ob der angegebene Assignee existiert und zum Board gehört.

    Bei partiellen Updates wird das bestehende Board verwendet, wenn kein neues
    Board in den Eingabedaten enthalten ist.
    """
    
    board = data.get("board")
    if board is None and self.instance is not None:
        board = self.instance.board

    assignee_id = data.get("assignee_id")

    if assignee_id is not None:
        try:
            assignee = User.objects.get(pk=assignee_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "assignee_id": "No assignee with that ID found."
            })

    if board and (
        board.owner_id != assignee.id
        and not board.members.filter(pk=assignee.id).exists()
    ):
        raise serializers.ValidationError({
            "assignee_id": "Assignee is not a boardmember."
        })
    
    return data


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate(self, data):
        """Validiert die Task-Daten einschließlich der Board-Zugehörigkeit des Assignees."""
        validate_board_user(self, data)
        return data
        
    def get_response(self, obj):
        """Erstellt die API-Darstellung eines Tasks samt Assignee und Reviewer."""

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
            "comments_count": obj.comments.count(),
        }

class SingleTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate(self, data): 
        """Validiert die Task-Daten einschließlich der Board-Zugehörigkeit des Assignees."""
        validate_board_user(self, data)
        return data

    def get_response(self, obj):
        """Erstellt die API-Darstellung eines einzelnen Tasks samt Benutzerdetails."""
            
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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]

    def validate(self, data):
        """Stellt sicher, dass der Kommentartext nicht leer ist."""
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