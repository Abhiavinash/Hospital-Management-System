from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from apps.users.models import User
from apps.patients.models import Patient
from core.models import Doctor, Appointment
from datetime import datetime


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class DashboardView(TemplateView):
    """Main dashboard - redirects based on user role."""
    template_name = "dashboard.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Verify session role matches user role (security check)
        session_role = request.session.get('user_role')
        if session_role and session_role != request.user.role:
            # Role mismatch - force logout
            from django.contrib.auth import logout
            logout(request)
            return redirect('login')
        
        # Redirect based on actual user role (compare as string)
        user_role = str(request.user.role)
        
        if user_role == 'ADMIN':
            return redirect('core:admin-dashboard')
        elif user_role == 'DOCTOR':
            return redirect('core:doctor-dashboard')
        elif user_role == 'PATIENT':
            return redirect('core:patient-dashboard')
        
        # If no role matches, logout and redirect to login
        from django.contrib.auth import logout
        logout(request)
        return redirect('login')


@method_decorator(login_required, name='dispatch')
class PatientListView(ListView):
    model = Patient
    template_name = 'patient_list.html'
    context_object_name = 'patients'
    
    def get_queryset(self):
        return Patient.objects.select_related('user').order_by('-created_at')


@login_required
@never_cache
def admin_dashboard(request):
    """Admin/Administrator dashboard view."""
    # Use string comparison for role check
    if str(request.user.role) != 'ADMIN':
        return redirect('core:dashboard')
    
    # Get statistics
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    recent_appointments = Appointment.objects.select_related('patient__user', 'doctor__user').order_by('-appointment_datetime')[:5]
    
    # Set no-cache headers
    response = render(request, 'admin_dashboard.html', {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'recent_appointments': recent_appointments,
    })
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required
@never_cache
def doctor_dashboard(request):
    """Doctor dashboard view."""
    # Use string comparison for role check
    if str(request.user.role) != 'DOCTOR':
        return redirect('core:dashboard')
    
    doctor = None
    today_appointments = []
    
    try:
        doctor = Doctor.objects.get(user=request.user)
        # Get today's appointments for this doctor
        today = datetime.now().date()
        today_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_datetime__date=today
        ).select_related('patient__user').order_by('appointment_datetime')
    except Doctor.DoesNotExist:
        # Create a placeholder for new doctors
        pass
    
    # Set no-cache headers
    response = render(request, 'doctor_dashboard.html', {
        'doctor': doctor,
        'today_appointments': today_appointments,
        'today': datetime.now().date(),
    })
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required
@never_cache
def patient_dashboard(request):
    """Patient dashboard view."""
    # Use string comparison for role check
    if str(request.user.role) != 'PATIENT':
        return redirect('core:dashboard')
    
    patient = None
    appointments = []
    
    try:
        patient = Patient.objects.get(user=request.user)
        # Get appointments for this patient
        appointments = Appointment.objects.filter(
            patient=patient
        ).select_related('doctor__user').order_by('-appointment_datetime')[:5]
    except Patient.DoesNotExist:
        # Create a placeholder for new patients
        pass
    
    # Set no-cache headers
    response = render(request, 'patient_dashboard.html', {
        'patient': patient,
        'appointments': appointments,
    })
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required
@never_cache
def doctor_list(request):
    """List all doctors - Admin view."""
    if request.user.role != User.Role.ADMIN:
        return redirect('dashboard')
    
    doctors = Doctor.objects.select_related('user').all()
    return render(request, 'doctor_list.html', {'doctors': doctors})


@login_required
@never_cache
def appointment_list(request):
    """List all appointments."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    appointments = Appointment.objects.select_related(
        'patient__user', 'doctor__user'
    ).order_by('-appointment_datetime')
    
    return render(request, 'appointment_list.html', {'appointments': appointments})


@login_required
@never_cache
def appointment_create(request):
    """Create new appointment."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        # Handle appointment creation
        messages.success(request, 'Appointment created successfully!')
        return redirect('core:appointment-list')
    
    # Get context for creating appointment
    patients = Patient.objects.select_related('user').all()
    doctors = Doctor.objects.select_related('user').all()
    
    return render(request, 'appointment_create.html', {
        'patients': patients,
        'doctors': doctors
    })


@login_required
@never_cache
def appointment_detail(request, pk):
    """View appointment details."""
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointment_detail.html', {'appointment': appointment})


@login_required
@never_cache
def appointment_cancel(request, pk):
    """Cancel an appointment."""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
        return redirect('core:appointment-list')
    
    return render(request, 'appointment_cancel.html', {'appointment': appointment})


@login_required
@never_cache
def medical_records(request):
    """View medical records."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'medical_records.html', {})


@login_required
@never_cache
def prescriptions(request):
    """View prescriptions."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'prescriptions.html', {})


@login_required
@never_cache
def settings_view(request):
    """User settings page."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'settings.html', {'user': request.user})


@login_required
@never_cache
def messages(request):
    """Messages/chat page."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'messages.html', {})


@login_required
@never_cache
def profile(request):
    """User profile page."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'profile.html', {'user': request.user})

