from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.db import transaction
from django.contrib import messages

from .models import Patient
from apps.users.models import User
from .forms import PatientUserForm, PatientProfileForm

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class PatientListView(ListView):
    """View to display a paginated list of patients."""
    model = Patient
    template_name = 'patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10

    def get_queryset(self):
        return Patient.objects.select_related('user').order_by('-created_at')

@login_required
@never_cache
def patient_register_view(request):
    """View to handle new patient registration."""
    if request.method == 'POST':
        user_form = PatientUserForm(request.POST)
        profile_form = PatientProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.role = User.Role.PATIENT
                user.save()

                patient_profile = profile_form.save(commit=False)
                patient_profile.user = user
                patient_profile.save()
            
            messages.success(request, f'Patient "{user.first_name} {user.last_name}" registered successfully!')
            return redirect('core:patient-list')
    else:
        user_form = PatientUserForm()
        profile_form = PatientProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'patient_register.html', context)

@login_required
@never_cache
def dashboard(request):
    """View for the dashboard."""
    return render(request, 'dashboard.html')
