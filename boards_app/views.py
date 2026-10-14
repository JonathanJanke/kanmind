from django.contrib.auth import authenticate
from django.db.models.aggregates import Count
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Board
from .serializers import BoardSerializer

def boards_with_counts():
    """
    Queryset, das alle Zähler direkt in der Datenbank berechnet.

    distinct=True ist nötig, weil der JOIN über members UND task_boards
    die Zeilen vervielfacht (Boards x Members x Tasks) und sonst falsche
    Summen entstehen würden.
    """
    return Board.objects.annotate(
        member_count=Count("members", distinct=True),
        # ticket_count=Count("task_boards", distinct=True),
        # tasks_to_do_count=Count(
        #     "task_boards",
        #     filter=Q(task_boards__status="TODO"),
        #     distinct=True,
        # ),
        # tasks_high_prio_count=Count(
        #     "task_boards",
        #     filter=Q(task_boards__priority="HIGH"),
        #     distinct=True,
        # ),
    )


class BoardListView(APIView):
    """
    View to create and list Boards
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        View for creating a Board
        """
        serializer = BoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save(owner_id=request.user.id)
        board = boards_with_counts().get(pk=board.pk)
        return Response(BoardSerializer(board).data, status=201)

    def get(self, request):
        """
        Alle Boards, bei denen der User Owner oder Member ist.
        Insgesamt nur eine einzige Datenbank-Query.
        """
        boards = (
            boards_with_counts()
            .filter(Q(owner_id=request.user.id) | Q(members=request.user.id))
            .distinct()
        )
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

class BoardDetailView(APIView):
    """
    View to retrieve, update and delete a Board
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        """
        View for retrieving a Board
        """
        try:
            board = boards_with_counts().get(pk=board_id)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=404)

        if not (board.owner_id == request.user.id or request.user in board.members.all()):
            return Response({"error": "You do not have permission to view this board"}, status=403)

        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def patch(self, request, board_id):
        """
        View for updating a Board
        """
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
        """
        View for deleting a Board
        """
        try:
            board = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=404)

        if board.owner_id != request.user.id:
            return Response({"error": "You do not have permission to delete this board"}, status=403)

        board.delete()
        return Response({"success": "Board deleted"}, status=204)

