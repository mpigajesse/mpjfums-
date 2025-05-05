# Utiliser l'image officielle de Python
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements.txt
COPY requirements.txt /app/
COPY shop/requirements.txt /app/shop_requirements.txt

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r shop_requirements.txt

# Installation explicite des packages problématiques
RUN pip install --no-cache-dir whitenoise==6.6.0
RUN pip install --no-cache-dir pillow
RUN pip install --no-cache-dir django-imagekit django-browser-reload
RUN pip install --no-cache-dir gunicorn

# Copier tout le code de l'application
COPY . /app/

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV PORT=8000

# Rendre le script manage.py exécutable
RUN chmod +x /app/shop/manage.py

# Créer structure de dossiers nécessaires
RUN mkdir -p /app/shop/staticfiles
RUN mkdir -p /app/shop/media

# Exécuter les commandes Django depuis le répertoire shop
WORKDIR /app/shop
RUN python manage.py makemigrations parfums || true
RUN python manage.py collectstatic --noinput || true

# Exposer le port
EXPOSE 8000

# Commande de démarrage avec vérification que le port est bien défini
CMD python -c "import os; port = os.environ.get('PORT', 8000); print(f'Starting on port {port}')" && \
    python manage.py migrate && \
    gunicorn --bind 0.0.0.0:${PORT:-8000} --workers=2 --timeout=120 shop.wsgi:application 