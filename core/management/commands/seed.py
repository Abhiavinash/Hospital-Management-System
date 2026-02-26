import random
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from faker import Faker
from apps.users.models import User
from core.models import Patient, Doctor, Appointment

class Command(BaseCommand):
    help = 'Seeds the database with dummy data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        # Clean up old data
        User.objects.exclude(is_superuser=True).delete()
        Patient.objects.all().delete()
        Doctor.objects.all().delete()
        Appointment.objects.all().delete()

        fake = Faker()

        # Create Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@hms.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin user created.'))

        # Create Doctors
        specializations = ['Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics', 'Dermatology']
        doctors = []
        for spec in specializations:
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"dr_{first_name.lower()}"
            if User.objects.filter(username=username).exists():
                username = f"{username}{random.randint(1,1000)}"

            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=f"{username}@hms.com",
                password=make_password('password123'),
                role='doctor'
            )
            doctor = Doctor.objects.create(
                user=user,
                specialization=spec,
                license_number=fake.unique.ean(length=13)
            )
            doctors.append(doctor)
        self.stdout.write(self.style.SUCCESS(f'{len(doctors)} doctors created.'))

        # Create Patients
        patients = []
        for _ in range(20):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"patient_{first_name.lower()}_{last_name.lower()}"
            if User.objects.filter(username=username).exists():
                username = f"{username}{random.randint(1,1000)}"

            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=f"{username}@patient.com",
                password=make_password('password123'),
                role='patient'
            )
            patient = Patient.objects.create(
                user=user,
                address=fake.address(),
                phone_number=fake.phone_number()
            )
            patients.append(patient)
        self.stdout.write(self.style.SUCCESS(f'{len(patients)} patients created.'))

        # Create Appointments
        for patient in patients:
            doctor = random.choice(doctors)
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_datetime=fake.date_time_this_year(after_now=True),
                reason=fake.sentence(nb_words=6)
            )
        self.stdout.write(self.style.SUCCESS(f'{len(patients)} appointments created.'))

        self.stdout.write(self.style.SUCCESS('Data seeding complete.'))
