# Utiliser l'image officielle de Python
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements.txt
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier tout le code de l'application
COPY . /app/

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV PORT=8000

# Exécuter les commandes Django
WORKDIR /app/shop
RUN python manage.py collectstatic --noinput || echo "Skipping collectstatic"

# Exposer le port pour Django
EXPOSE 8000

# Commande de démarrage
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT 