from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Board
from .serializers import BoardSerializer

class BoardListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(owner_id=request.user.id)
        board_data = [BoardSerializer().get_response(board) for board in boards]
        return Response(board_data)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
