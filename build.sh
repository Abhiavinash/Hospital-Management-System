#!/bin/bash
# Build script for Render deployment
# This script runs during the build phase to set up the database and static files

set -e

echo "Running migrations..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Build complete!"

