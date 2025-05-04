from django.shortcuts import render, get_object_or_404
from .models import Parfum, Categorie

def accueil(request):
    parfums = Parfum.objects.all()[:6]  # Limité à 6 parfums pour la page d'accueil
    categories = Categorie.objects.all()
    return render(request, 'parfums/accueil.html', {
        'parfums': parfums, 
        'categories': categories
    })

def liste_parfums(request):
    parfums = Parfum.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'parfums/liste_parfums.html', {
        'parfums': parfums, 
        'categories': categories
    })

def detail_parfum(request, parfum_id):
    parfum = get_object_or_404(Parfum, id=parfum_id)
    return render(request, 'parfums/detail_parfum.html', {'parfum': parfum})

def parfums_par_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    parfums = Parfum.objects.filter(categorie=categorie)
    categories = Categorie.objects.all()
    return render(request, 'parfums/liste_parfums.html', {
        'parfums': parfums, 
        'categorie_active': categorie,
        'categories': categories
    })
