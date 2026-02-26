from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('admin/', views.admin_dashboard, name='admin-dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor-dashboard'),
    path('patient/', views.patient_dashboard, name='patient-dashboard'),
    path('patients/list/', views.PatientListView.as_view(), name='patient-list'),
    path('doctors/', views.doctor_list, name='doctor-list'),
    path('appointments/', views.appointment_list, name='appointment-list'),
    path('appointments/create/', views.appointment_create, name='appointment-create'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment-detail'),
    path('appointments/<int:pk>/cancel/', views.appointment_cancel, name='appointment-cancel'),
    path('medical-records/', views.medical_records, name='medical-records'),
    path('prescriptions/', views.prescriptions, name='prescriptions'),
    path('settings/', views.settings_view, name='settings'),
    path('messages/', views.messages, name='messages'),
    path('profile/', views.profile, name='profile'),
]

