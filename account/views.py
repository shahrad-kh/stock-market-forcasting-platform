from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsUnauthenticated
from .serializers import LoginSerializer, SignUpSerializer


class SignUpView(APIView):
    """
    API endpoint for user registration.
    """
    
    permission_classes = [AllowAny]


    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint for user login.
    """
    
    permission_classes = [IsUnauthenticated]


    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)  # Log in the user
            return Response({"message": "Logged in successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    API endpoint for user logout.
    """
    
    permission_classes = [IsAuthenticated]

    
    def get(self, request):
        logout(request)  # Log out the user
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
