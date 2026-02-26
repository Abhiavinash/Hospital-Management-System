from rest_framework import serializers
from .models import Patient, PatientDocument

class PatientDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDocument
        fields = ['id', 'document', 'description', 'uploaded_at']

class PatientSerializer(serializers.ModelSerializer):
    documents = PatientDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Patient
        fields = '__all__'