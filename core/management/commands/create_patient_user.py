from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from apps.users.models import User
from core.models import Patient


class Command(BaseCommand):
    help = 'Creates a patient user with credentials: patient / 123'

    def handle(self, *args, **options):
        username = 'patient'
        password = '123'
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
            user = User.objects.get(username=username)
        else:
            # Create the user
            user = User.objects.create(
                username=username,
                first_name='Patient',
                last_name='User',
                email='patient@hms.com',
                password=make_password(password),
                role=User.Role.PATIENT
            )
            self.stdout.write(self.style.SUCCESS(f'User "{username}" created.'))
        
        # Create or get Patient profile
        patient, created = Patient.objects.get_or_create(
            user=user,
            defaults={
                'address': '123 Main Street',
                'phone_number': '1234567890'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Patient profile created for "{username}".'))
        else:
            self.stdout.write(self.style.WARNING(f'Patient profile already exists for "{username}".'))
        
        self.stdout.write(self.style.SUCCESS(
            f'Patient credentials created: username="{username}", password="{password}"'
        ))

