from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from .models import User
from .serializers import LoginSerializer, UserRegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """Registriert einen Benutzer und gibt dessen Profildaten samt Auth-Token zurück."""
        serializer = UserRegisterSerializer(data=request.data)
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
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Authentifiziert einen Benutzer und gibt bei Erfolg dessen Auth-Token zurück."""
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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def email_check(request, email):
    """Sucht einen Benutzer per E-Mail und gibt dessen öffentliche Profildaten zurück."""
    user = User.objects.filter(email=email).first()
    if user:
        return Response(
            {
                "id": user.id,
                "email": user.email,
                "fullname": user.fullname,
            },
            status=status.HTTP_200_OK,
        )
    return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)