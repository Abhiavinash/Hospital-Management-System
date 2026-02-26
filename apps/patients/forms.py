from django import forms
from apps.users.models import User
from .models import Patient

class PatientUserForm(forms.ModelForm):
    """Form for creating a user account for a patient."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'username': 'This will be used for the patient to log in.',
        }

class PatientProfileForm(forms.ModelForm):
    """Form for the patient's profile details."""
    class Meta:
        model = Patient
        fields = ['photo', 'phone_number', 'address', 'date_of_birth', 
                  'emergency_contact_name', 'emergency_contact_phone', 
                  'insurance_provider', 'insurance_policy_number']