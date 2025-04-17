from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Appointment
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny

 

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'title', 'description', 'date_time', 'status', 'user', 'name', 'family_name']
 


class UserSerializer(serializers.ModelSerializer):
    # Nested serializer for appointments
    appointments = AppointmentSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'appointments')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")