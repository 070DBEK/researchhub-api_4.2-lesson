#!/bin/bash

# Build script for Vercel
echo "BUILD START"

# Install production dependencies
python3.9 -m pip install -r requirements/production.txt

# Set Django settings for production
export DJANGO_SETTINGS_MODULE=config.settings.production

# Collect static files
python3.9 manage.py collectstatic --noinput --clear

echo "BUILD END"