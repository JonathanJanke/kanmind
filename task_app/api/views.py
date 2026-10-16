from django.db.models import Count
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication_app.models import User
from boards_app.models import Board

from ..models import Comment, Task
from .serializers import CommentSerializer, SingleTaskSerializer, TaskSerializer


def task_response_queryset():
    return (
        Task.objects.select_related("assignee", "reviewer")
        .annotate(comments_count=Count("comments"))
    )


def get_task_with_board(task_id):
    return Task.objects.select_related("board").filter(pk=task_id).first()


def user_can_access_board(user, board):
    return board.owner_id == user.pk or board.members.filter(pk=user.pk).exists()


def resolve_task_relations(board, validated_data):
    errors = {}
    for name in ("assignee", "reviewer"):
        user = validated_data.get(name)
        if user is None:
            continue
        if user.pk != board.owner_id and not board.members.filter(pk=user.pk).exists():
            errors[f"{name}_id"] = "A user is not a board member."

    if errors:
        raise ValidationError(errors)


class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Erstellt einen Task und gibt ihn mit den zugehörigen Benutzerdaten zurück."""
        serializer = TaskSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            board = Board.objects.get(pk=serializer.validated_data["board_id"])
        except Board.DoesNotExist:
            return Response({"error": "Board not found."}, status=status.HTTP_404_NOT_FOUND)

        if not user_can_access_board(request.user, board):
            return Response({"error": "Not a member of this board."}, status=status.HTTP_403_FORBIDDEN)

        try:
            resolve_task_relations(board, serializer.validated_data)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

        task = serializer.save(creator=request.user)
        task = task_response_queryset().get(pk=task.pk)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)


class AssignedToUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Gibt alle Tasks zurück, die dem angemeldeten Benutzer zugewiesen sind."""
        tasks = task_response_queryset().filter(assignee=request.user)
        return Response(TaskSerializer(tasks, many=True).data, status=status.HTTP_200_OK)


class ReviewingToUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Gibt alle Tasks zurück, bei denen der Benutzer als Reviewer eingetragen ist."""
        tasks = task_response_queryset().filter(reviewer=request.user)
        return Response(TaskSerializer(tasks, many=True).data, status=status.HTTP_200_OK)


class SingleTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_id):
        """Aktualisiert einen Task teilweise und liefert bei Erfolg den aktualisierten Task."""
        task = get_task_with_board(task_id)
        if task is None:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        if not user_can_access_board(request.user, task.board):
            return Response({"error": "Not a member of this board."}, status=status.HTTP_403_FORBIDDEN)

        if "board" in request.data and str(request.data["board"]) != str(task.board_id):
            return Response(
                {"board": ["Changing the board is not allowed."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SingleTaskSerializer(
            task,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            resolve_task_relations(task.board, serializer.validated_data)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

        updated_task = serializer.save()
        updated_task = task_response_queryset().get(pk=updated_task.pk)
        return Response(
            SingleTaskSerializer(updated_task).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, task_id):
        """Löscht den angegebenen Task oder antwortet mit 404, falls er nicht existiert."""
        task = get_task_with_board(task_id)
        if task is None:
            return Response({"error": "Wrong task id."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.pk not in (task.creator_id, task.board.owner_id):
            return Response(
                {"error": "Only the creator or the board owner can delete this task."},
                status=status.HTTP_403_FORBIDDEN,
            )

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        """Gibt alle Kommentare zurück, die zum angegebenen Task gehören."""
        task = get_task_with_board(task_id)
        if task is None:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        if not user_can_access_board(request.user, task.board):
            return Response({"error": "Not a member of this board."}, status=status.HTTP_403_FORBIDDEN)

        comments = Comment.objects.filter(task_id=task_id).select_related("author")
        return Response(
            CommentSerializer(comments, many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request, task_id):
        """Erstellt einen Kommentar für den Task und setzt den Autor auf den angemeldeten Benutzer."""
        task = get_task_with_board(task_id)
        if task is None:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        if not user_can_access_board(request.user, task.board):
            return Response({"error": "Not a member of this board."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(task=task, author=request.user)
            return Response(
                CommentSerializer(comment).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id, comment_id):
        """Löscht einen Kommentar des Tasks oder antwortet mit 404, falls er nicht gefunden wird."""
        try:
            comment = Comment.objects.get(pk=comment_id, task_id=task_id)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        if comment.author_id != request.user.pk:
            return Response(
                {"error": "Only the author can delete this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
