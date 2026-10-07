from rest_framework.response import Response
from rest_framework import status
from authentication_app.models import User
from kanmind.api.serializers import LoginSerializer, UserSerializer
from rest_framework.views import APIView

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User(**serializer.validated_data)
            user.save()

            return Response(serializer.get_response(user), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        password = request.data.get('password')

        if serializer.is_valid():
                if User.objects.filter(email=serializer.validated_data['email']).exists():
                    
                    user = User.objects.get(email=serializer.validated_data['email'])
                    if user.password == password:
                        return Response(serializer.get_response(user), status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Serializer invalid', 'details': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

