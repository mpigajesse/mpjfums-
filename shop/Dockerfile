# Utiliser l'image officielle de Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt /app/

RUN pip install -r requirements.txt

# Copier tout le code de l'application dans le conteneur
COPY . /app/

# Exposer le port 8000 pour Django
EXPOSE 8000

# Commande par défaut pour démarrer l'application Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 