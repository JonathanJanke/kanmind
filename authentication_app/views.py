from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication_app.models import User
from kanmind.api.serializers import LoginSerializer, UserSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)

        user_data = serializer.validated_data.copy()
        user_data.pop("repeat_password")
        raw_password = user_data.pop("password")

        if User.objects.filter(email=user_data["email"]).exists():
            return Response(
                {"error": "Invalid request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User(**user_data)
        user.set_password(raw_password)
        user.save()

        return Response(
            serializer.get_response(user),
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            request=request,
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response(
                {"error": "Invalid request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.get_response(user), status=status.HTTP_200_OK)
