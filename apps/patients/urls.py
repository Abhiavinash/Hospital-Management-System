from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('register/', views.patient_register_view, name='patient-register'),
]

