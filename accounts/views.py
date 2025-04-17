from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth import login
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer, AppointmentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from .models import Appointment
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied
from django.contrib.auth.models import Group

class UserAppointmentsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):
        try:
            # Ensure the user exists
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Get all appointments for the specified user
        appointments = Appointment.objects.filter(user=user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
class UserAppointmentsViewc(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get all appointments for the authenticated user
        appointments = Appointment.objects.filter(user=request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
class UpdateAppointmentStatusView(APIView):
    ##permission_classes = [IsAdminUser]  # Only admins can update the status
    permission_classes = [AllowAny]
    def patch(self, request, appointment_id):
        try:
            # Get the appointment
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=404)

        # Get the new status from the request data
        new_status = request.data.get('status')

        # Validate the status
        if new_status not in ['ACCEPTED', 'REFUSED']:
            return Response({"error": "Invalid status"}, status=400)

        # Update the status
        appointment.status = new_status
        appointment.save()

        # Return the updated appointment
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=200)

class CreateAppointmentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, user_id):
        try:
            # Ensure the user exists
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Add the user ID to the request data
        data = request.data.copy()
        data['user'] = user.id

        # Validate and save the appointment
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    


class UserListView(APIView):
    ##permission_classes = [IsAdminUser]  # Only admins can access this view
    permission_classes = [AllowAny]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

 
        
class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully."
        })

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Check if the user belongs to the "Admin" group
            is_admin = user.groups.filter(name='Admin').exists()

            # Serialize the user data, including appointments (if needed)
            # Replace `UserSerializer` with your actual serializer
            serializer = UserSerializer(user)

            # Return different responses based on group membership
            if is_admin:
                return Response({
                    'message': 'Login Admin successful',
                    'user': serializer.data,
                    'token': 'your_generated_token_here',  # Replace with your actual token generation logic
                    'redirect_to': '/DashboardAdmin'  # Redirect to admin dashboard
                }, status=200)
            else:
                return Response({
                    'message': 'Login user successful',
                    'user': serializer.data,
                    'token': 'your_generated_token_here',  # Replace with your actual token generation logic
                    'redirect_to': '/user-dashboard/'  # Redirect to user dashboard
                }, status=200)
        else:
            return Response({'message': 'Invalid credentials'}, status=401)