from django.contrib.auth import authenticate
from django.db.models.aggregates import Count
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Board
from .serializers import BoardSerializer

def boards_with_counts():
    """Liefert Boards mit in der Datenbank berechneter Mitgliederanzahl.

    `distinct=True` verhindert doppelte Mitgliederzählungen durch JOINs.
    """
    return Board.objects.annotate(
        member_count=Count("members", distinct=True),
        ticket_count=Count("tasks", distinct=True),
        tasks_to_do_count=Count(
            "tasks",
            filter=Q(tasks__status="to-do"),
            distinct=True,
        ),
        tasks_in_progress_count=Count(
            "tasks",
            filter=Q(tasks__status="in-progress"),
            distinct=True,
        ),
        tasks_done_count=Count(
            "tasks",
            filter=Q(tasks__status="done"),
            distinct=True,
        ),
        tasks_in_review_count=Count(
            "tasks",
            filter=Q(tasks__status="review"),
            distinct=True,
        ),
        tasks_high_prio_count=Count(
            "tasks",
            filter=Q(tasks__priority="high"),
            distinct=True,
        ),
        tasks_medium_prio_count=Count(
            "tasks",
            filter=Q(tasks__priority="medium"),
            distinct=True,
        ),
        tasks_low_prio_count=Count(
            "tasks",
            filter=Q(tasks__priority="low"),
            distinct=True,
        ),
    )


class BoardListView(APIView):
    """
    View to create and list Boards
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Erstellt ein Board mit dem angemeldeten Benutzer als Owner."""
        serializer = BoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save(owner_id=request.user.id)
        board = boards_with_counts().get(pk=board.pk)
        return Response(BoardSerializer.get_response(BoardSerializer(board)), status=201)
    

    def get(self, request):
        """Listet die Boards, bei denen der Benutzer Owner oder Mitglied ist."""
        boards = (
            boards_with_counts()
            .filter(Q(owner_id=request.user.id) | Q(members=request.user.id))
            .distinct()
        )
        return Response([BoardSerializer.get_response(BoardSerializer(board)) for board in boards])

class BoardDetailView(APIView):
    """
    View to retrieve, update and delete a Board
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        """Gibt ein Board zurück, sofern der Benutzer Owner oder Mitglied ist."""
        try:
            board = boards_with_counts().get(pk=board_id)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=404)

        if not (board.owner_id == request.user.id or request.user in board.members.all()):
            return Response({"error": "You do not have permission to view this board"}, status=403)

        return Response(BoardSerializer.get_detail_response(BoardSerializer(board)))

    def patch(self, request, board_id):
        """Aktualisiert ein Board teilweise; Änderungen sind nur dem Owner erlaubt."""
        try:
            board = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=404)

        if board.owner_id != request.user.id:
            return Response({"error": "You do not have permission to update this board"}, status=403)

        serializer = BoardSerializer(board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, board_id):
        """Löscht ein Board, sofern der angemeldete Benutzer dessen Owner ist."""
        try:
            board = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=404)

        if board.owner_id != request.user.id:
            return Response({"error": "You do not have permission to delete this board"}, status=403)

        board.delete()
        return Response({"success": "Board deleted"}, status=204)
