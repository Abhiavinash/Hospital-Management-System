from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import User
from .models import Patient, Doctor, Appointment

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
