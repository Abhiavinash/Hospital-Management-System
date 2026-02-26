import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

def patient_photo_upload_path(instance, filename):
    """Generates a unique path for patient photos."""
    return f'patients/{instance.patient_id}/photos/{filename}'

def patient_document_upload_path(instance, filename):
    """Generates a unique path for patient documents."""
    return f'patients/{instance.patient.patient_id}/documents/{filename}'


class Patient(models.Model):
    """
    Model to store patient data.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    patient_id = models.CharField(max_length=100, unique=True, blank=True)
    photo = models.ImageField(_("Profile Photo"), upload_to=patient_photo_upload_path, null=True, blank=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True)
    address = models.TextField(_("Address"), blank=True)
    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)
    emergency_contact_name = models.CharField(_("Emergency Contact Name"), max_length=100, blank=True)
    emergency_contact_phone = models.CharField(_("Emergency Contact Phone"), max_length=20, blank=True)
    insurance_provider = models.CharField(_("Insurance Provider"), max_length=100, blank=True)
    insurance_policy_number = models.CharField(_("Insurance Policy Number"), max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Generate a unique patient ID, e.g., HMS-2024-XXXXX
            last_patient = Patient.objects.order_by('id').last()
            new_id = (last_patient.id + 1) if last_patient else 1
            year = timezone.now().year
            self.patient_id = f'HMS-{year}-{new_id:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.patient_id})"


class PatientDocument(models.Model):
    """
    Model to store uploaded documents for a patient.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(_("Document"), upload_to=patient_document_upload_path)
    description = models.CharField(_("Description"), max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)