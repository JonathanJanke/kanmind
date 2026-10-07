from rest_framework.response import Response
from rest_framework import status
from authentication_app.models import User
from .serializers import LoginSerializer, UserSerializer
from rest_framework.views import APIView

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the user already exists
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new user
            user = User(**serializer.validated_data)
            user.save()

            return Response(serializer.get_response(user), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        email = request.data.get('email')
        password = request.data.get('password')

        if serializer.is_valid():
                if User.objects.filter(email=serializer.validated_data['email']).exists():
                    try:
                        user = User.objects.get(email=email)
                        if user.password == password:
                            return Response(UserSerializer().get_response(user), status=status.HTTP_200_OK)
                        else:
                            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
                    except User.DoesNotExist:
                        return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Internal Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)