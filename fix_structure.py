import os
import shutil
from pathlib import Path

# Base directory of the project
BASE_DIR = Path.cwd()
APPS_DIR = BASE_DIR / 'apps'
TEMPLATES_DIR = BASE_DIR / 'templates'

def fix_project_structure():
    print("Starting project restructuring...")

    # 1. Create the 'apps' directory and its __init__.py
    if not APPS_DIR.exists():
        APPS_DIR.mkdir()
        print(f"Created directory: {APPS_DIR}")
    (APPS_DIR / '__init__.py').touch()

    # 2. Create sub-app directories (core, users, patients)
    for app in ['core', 'users', 'patients']:
        app_path = APPS_DIR / app
        if not app_path.exists():
            app_path.mkdir()
            print(f"Created app directory: {app_path}")
        (app_path / '__init__.py').touch()

    # 3. Move Python logic files from templates/ to apps/patients/
    # These files belong in the app logic, not in templates
    files_to_move = ['views.py', 'models.py', 'forms.py', 'urls.py', 'serializers.py']
    
    for filename in files_to_move:
        src = TEMPLATES_DIR / filename
        dst = APPS_DIR / 'patients' / filename
        
        if src.exists():
            shutil.move(str(src), str(dst))
            print(f"Moved {filename} to apps/patients/")

    # 4. Create apps/users/models.py (Required by views.py)
    users_models = APPS_DIR / 'users' / 'models.py'
    if not users_models.exists():
        with open(users_models, 'w') as f:
            f.write("from django.contrib.auth.models import AbstractUser\n")
            f.write("from django.db import models\n\n")
            f.write("class User(AbstractUser):\n")
            f.write("    class Role(models.TextChoices):\n")
            f.write("        ADMIN = 'ADMIN', 'Admin'\n")
            f.write("        DOCTOR = 'DOCTOR', 'Doctor'\n")
            f.write("        PATIENT = 'PATIENT', 'Patient'\n\n")
            f.write("    role = models.CharField(max_length=50, choices=Role.choices, default=Role.PATIENT)\n")
        print("Created apps/users/models.py")

    # 5. Create apps/core/urls.py (Required by main urls.py)
    core_urls = APPS_DIR / 'core' / 'urls.py'
    if not core_urls.exists():
        with open(core_urls, 'w') as f:
            f.write("from django.urls import path\n\nurlpatterns = []\n")
        print("Created apps/core/urls.py")

    print("\nStructure fixed successfully!")

if __name__ == "__main__":
    fix_project_structure()