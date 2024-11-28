from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    def create(self, validated_data):
        
        # to create new user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        
        # user info validation
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        return user
