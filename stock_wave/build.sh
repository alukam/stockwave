#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Collect static files (Fixes the "Not Found" CSS/JS issues)
python manage.py collectstatic --no-input

# 3. Apply database migrations
python manage.py migrate

# 4. Create an Admin User Automatically (Crucial!)
# This checks if an admin exists; if not, it creates one using environment variables.
python manage.py shell << END
from users.models import User
import os
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', os.environ.get('ADMIN_PASSWORD', 'Stockwave2026!'))
    print("Admin user created successfully.")
else:
    print("Admin user already exists.")
END