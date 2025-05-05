# Utiliser l'image officielle de Python
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements.txt
COPY requirements.txt /app/
COPY shop/requirements.txt /app/shop/

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r shop/requirements.txt

# Installation explicite des packages problématiques
RUN pip install --no-cache-dir whitenoise==6.6.0
RUN pip install --no-cache-dir pillow
RUN pip install --no-cache-dir django-imagekit django-browser-reload

# Copier tout le code de l'application
COPY . /app/

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV PORT=8000

# Changer vers le répertoire de l'application
WORKDIR /app/shop

# Exécuter les commandes Django
RUN python manage.py makemigrations parfums || true
RUN python manage.py collectstatic --noinput || true

# Exposer le port pour Django
EXPOSE 8000

# Commande de démarrage
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT 