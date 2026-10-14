from django.shortcuts import render
from .models import Task    
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer.get_response(serializer, task), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class AssignedToUserView(APIView):
    """
    View to retrieve every task, this User is assigned to
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        View for retrieving every task, this User is assigned to
        """
        tasks = Task.objects.filter(assignee_id=request.user.id)
        serializer = TaskSerializer()

        data = [serializer.get_response(task) for task in tasks]
        return Response(data, status=status.HTTP_200_OK)

class ReviewingToUserView(APIView):
    """
    View to retrieve every task, this User is assigned to
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        View for retrieving every task, this User is assigned to
        """
        tasks = Task.objects.filter(reviewer_id=request.user.id)
        serializer = TaskSerializer()

        data = [serializer.get_response(task) for task in tasks]
        return Response(data, status=status.HTTP_200_OK)
    