from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.users.models import User


@never_cache
def custom_login(request):
    """Custom login view with role-based authentication."""
    # If already authenticated, redirect to dashboard (but first check if we need to clear old session)
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Clear any existing session data before login
            request.session.flush()
            
            # Login the user
            login(request, user)
            
            # Store user role in session for extra security
            request.session['user_role'] = user.role
            request.session['user_id'] = user.id
            
            # Redirect based on role
            if user.role == User.Role.ADMIN:
                return redirect('core:admin-dashboard')
            elif user.role == User.Role.DOCTOR:
                return redirect('core:doctor-dashboard')
            elif user.role == User.Role.PATIENT:
                return redirect('core:patient-dashboard')
            else:
                messages.error(request, 'Invalid user role. Please contact administrator.')
                # Logout if no valid role
                from django.contrib.auth import logout
                logout(request)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


@never_cache
def home(request):
    """Home page - redirects to login or dashboard based on auth status."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return redirect('login')


@never_cache
def patient_login(request):
    """Patient login view - redirects to main login page with patient tab active."""
    return redirect('login')


@never_cache
def doctor_login(request):
    """Doctor login view - redirects to main login page with doctor tab active."""
    return redirect('login')


@login_required
@never_cache
def dashboard(request):
    """Main dashboard view - redirects based on user role."""
    # Use string comparison for role check
    user_role = str(request.user.role)
    
    if user_role == 'ADMIN':
        return redirect('core:admin-dashboard')
    elif user_role == 'DOCTOR':
        return redirect('core:doctor-dashboard')
    elif user_role == 'PATIENT':
        return redirect('core:patient-dashboard')
    return redirect('login')


@login_required
@never_cache
def admin_dashboard(request):
    """Admin dashboard view."""
    # Use string comparison for role check
    if str(request.user.role) != 'ADMIN':
        return redirect('core:dashboard')
    return render(request, 'admin_dashboard.html')


@login_required
@never_cache
def doctor_dashboard(request):
    """Doctor dashboard view."""
    # Use string comparison for role check
    if str(request.user.role) != 'DOCTOR':
        return redirect('core:dashboard')
    return render(request, 'doctor_dashboard.html')


@login_required
@never_cache
def patient_dashboard(request):
    """Patient dashboard view."""
    # Use string comparison for role check
    if str(request.user.role) != 'PATIENT':
        return redirect('core:dashboard')
    return render(request, 'patient_dashboard.html')


@never_cache
def custom_logout(request):
    """Custom logout view with proper session and cache clearing."""
    from django.contrib.auth import logout as auth_logout
    
    # Store the reference to session before flushing
    # Clear all session data
    request.session.flush()
    
    # Clear all cookie data
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    # Also clear the session cookie explicitly
    response.set_cookie('sessionid', '', expires='Thu, 01 Jan 1970 00:00:00 GMT', path='/')
    response.set_cookie('csrftoken', '', expires='Thu, 01 Jan 1970 00:00:00 GMT', path='/')
    
    # Logout the user
    auth_logout(request)
    
    return response

