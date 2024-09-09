#!/usr/bin/env bash
# Exit on error
set -o errexit
apt-get update && apt-get install -y \
  libcairo2 \
  libcairo2-dev \
  pkg-config \
  python3-dev
# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate