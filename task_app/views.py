from django.shortcuts import render
from .models import Comment, Task    
from .serializers import TaskSerializer, SingleTaskSerializer, CommentSerializer
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

    
class SingleTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_id):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SingleTaskSerializer(task, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            updated_task = serializer.save()
            return Response(SingleTaskSerializer.get_response(serializer, updated_task), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, task_id):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Wrong task id."}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        comments = Comment.objects.filter(task_id=task_id)
        serializer = CommentSerializer(comments, many=True)
        return Response([CommentSerializer.get_response(serializer, comment) for comment in comments], status=status.HTTP_200_OK)

    def post(self, request, task_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task_id=task_id, author=request.user)
            return Response(CommentSerializer.get_response(serializer, serializer.instance), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id, task_id=task_id)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)