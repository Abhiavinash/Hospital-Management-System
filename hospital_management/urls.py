"""
URL configuration for hospital_management project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('patient-login/', views.patient_login, name='patient-login'),
    path('doctor-login/', views.doctor_login, name='doctor-login'),
    path('dashboard/', include('core.urls')),
    path('patients/', include('apps.patients.urls')),
]

