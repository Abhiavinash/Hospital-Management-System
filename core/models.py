from django.db import models
from django.conf import settings

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to='patient_profile_pics/', null=True, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    medical_history = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to='doctor_profile_pics/', null=True, blank=True)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    availability = models.JSONField(default=dict) # e.g., {'Monday': ['09:00-12:00', '14:00-17:00']}

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialization})"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_datetime = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.last_name} for {self.patient.user.last_name} on {self.appointment_datetime.strftime('%Y-%m-%d %H:%M')}"
