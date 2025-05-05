#!/bin/bash

# Obtenir le port à utiliser (par défaut 8000 si PORT n'est pas défini)
PORT=${PORT:-8000}
echo "Démarrage du serveur sur le port $PORT"

cd shop

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate --noinput

# Démarrer Gunicorn avec le port défini dans l'environnement
echo "Démarrage de Gunicorn..."
gunicorn shop.wsgi:application --bind 0.0.0.0:$PORT --workers 2 