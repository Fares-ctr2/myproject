from django.urls import path, include
##from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView,UserListView, UserAppointmentsView,CreateAppointmentView
from .views import UpdateAppointmentStatusView, UserAppointmentsViewc


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/appointments/', UserAppointmentsView.as_view(), name='user-appointments'),
    path('users/<int:user_id>/appointments/', UserAppointmentsViewc.as_view(), name='user-appointments'),
    path('users/<int:user_id>/appointments/create/',CreateAppointmentView.as_view() , name='create-appointment1'),
    path('appointments/<int:appointment_id>/update-status/', UpdateAppointmentStatusView.as_view(), name='update-appointment-status'),
   
]