from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Board
from .serializers import BoardSerializer

class BoardListView(APIView):
    def get(self, request):
        serializer = BoardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        boards = Board.objects.all()
        board_data = [serializer.get_response(board) for board in boards]
        return Response(board_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
