from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REFUSED', 'Refused'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255, )  
    family_name = models.CharField(max_length=255, )  
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )


    def __str__(self):
        return f"{self.title} - {self.get_status_display()} ({self.name or 'No Name'} {self.family_name or 'No Family Name'})"