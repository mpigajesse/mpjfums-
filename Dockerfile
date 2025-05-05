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
# Le port sera défini par Railway

# Exécuter les commandes Django depuis le répertoire shop
RUN cd /app/shop && python manage.py makemigrations parfums || true
RUN cd /app/shop && python manage.py collectstatic --noinput || true

# Exposer le port dynamique fourni par Railway
EXPOSE $PORT

# Commande de démarrage
CMD cd /app/shop && python manage.py migrate && gunicorn shop.wsgi:application --bind 0.0.0.0:$PORT --workers=3 --timeout=120 --access-logfile=- --error-logfile=- --log-level=info 