# MPJFUMS - Parfumerie Gabonaise en ligne

MPJFUMS est une application web de gestion de parfumerie, conçue pour le marché gabonais et bâtie avec Django. Ce projet propose une base solide et gratuite pour toute personne ou entreprise souhaitant continuer ou personnaliser une boutique de parfums en ligne. Les échantillons fournis sont des exemples de base pour démarrer votre propre plateforme.

## 🌟 Fonctionnalités principales

- Catalogue de parfums catégorisés
- Optimisation automatique des images via django-imagekit
- Interface d’administration améliorée
- Multilingue (français par défaut)
- Interface responsive (mobile & desktop)
- Gestion des stocks et commandes de base
- Déploiement simplifié sur Railway

## 🚀 Technologies utilisées

- **Backend:** Django 5.2
- **Base de données:** PostgreSQL (prod.) / SQLite (dev.)
- **Conteneurisation :** Docker & Docker Compose
- **CI/CD :** GitHub Actions, Railway
- **Monitoring :** Sentry
- **Gestion des fichiers statiques:** WhiteNoise
- **Optimisation des performances:** Cache (django-cache-memoize), traitement images

## 🔥 Démarrer rapidement

### Prérequis
- Python 3.10+
- (Optionnel) Docker & Docker Compose

### Installation locale

```bash
git clone https://github.com/mpigajesse/mpjfums-.git
cd mpjfums-
pip install -r requirements.txt
cd shop && python manage.py migrate
python manage.py runserver
```

### Avec Docker
```bash
docker-compose -f shop/docker-compose.yml up
```
Ouvrez http://localhost:8000

## 📦 Déploiement

Le projet est prêt à être déployé sur Railway. Consultez [railwaydoc.md](railwaydoc.md) pour les étapes détaillées.

## 🧪 Tests

```bash
cd shop
python manage.py test
```

## 📚 Documentation

- Guide Railway: [railwaydoc.md](railwaydoc.md)
- Pipeline CI/CD: [CICD.md](CICD.md)

## 🤝 Contribution

Ce dépôt propose des échantillons de base, entièrement gratuits pour toute utilisation ou extension. Vous pouvez donc l’utiliser comme base pour vos propres projets de boutique de parfum ou e-commerce, et continuer de l’améliorer selon vos besoins. Les contributions (issues, pull requests) sont encouragées !

## 📝 Licence

Projet sous licence [MIT](LICENSE).

---
> **Remarque :** Ce projet fournit un socle solide, gratuit et prêt à être personnalisé par toute personne désireuse de poursuivre ou d’étendre la solution. Profitez-en pour démarrer rapidement votre boutique en ligne !
