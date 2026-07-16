#!/usr/bin/env bash
# CalmRio — Django project setup
# Usage: bash scripts/setup.sh

set -euo pipefail

echo "=== CalmRio Django Setup ==="

# 1. Python environment
if [ ! -d "venv" ]; then
    echo "→ Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

# 2. Install dependencies
echo "→ Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Environment file
if [ ! -f ".env" ]; then
    echo "→ Creating .env file with secret key..."
    SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    cat > .env << EOF
DJANGO_SECRET_KEY=$SECRET
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
EOF
    echo "   → .env created"
fi

# 4. Run migrations
echo "→ Running database migrations..."
python manage.py migrate

# 5. Create superuser (optional)
echo ""
echo "→ Create admin superuser? (Ctrl+C to skip)"
python manage.py createsuperuser --email admin@calm-rio.com --username admin 2>/dev/null || true

# 6. Collect static files
echo "→ Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Start the dev server:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Admin panel: http://127.0.0.1:8000/admin/"
