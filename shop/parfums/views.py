from django.shortcuts import render, get_object_or_404, redirect
from .models import Parfum, Categorie
from django.http import HttpResponseServerError, HttpResponse
from django.core.cache import cache
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page
from django.utils.cache import patch_response_headers
from django.urls import reverse

@cache_page(60 * 15)  # Cache pour 15 minutes
def accueil(request):
    try:
        # Récupération des parfums mis en avant ou récents, avec prefetch pour réduire les requêtes
        featured_parfums = Parfum.objects.filter(featured=True).select_related('categorie')[:3]
        recent_parfums = Parfum.objects.order_by('-date_ajout').select_related('categorie')[:3]
        
        # Si pas assez de parfums mis en avant, compléter avec des récents
        if featured_parfums.count() < 3:
            needed = 3 - featured_parfums.count()
            for p in recent_parfums[:needed]:
                if p not in featured_parfums:
                    featured_parfums = list(featured_parfums) + [p]
            featured_parfums = featured_parfums[:3]
        
        # Récupérer les catégories avec un comptage optimisé de parfums
        cache_key = 'all_categories'
        categories = cache.get(cache_key)
        if not categories:
            categories = Categorie.objects.all()
            cache.set(cache_key, categories, 3600)  # Cache pour 1 heure
        
        # Rendu de la réponse avec ajout d'en-têtes de cache
        response = render(request, 'parfums/accueil.html', {
            'featured_parfums': featured_parfums,
            'recent_parfums': recent_parfums,
            'categories': categories
        })
        patch_response_headers(response, cache_timeout=60 * 15)
        return response
    except Exception as e:
        # Gérer les erreurs de façon élégante
        print(f"Erreur sur la page d'accueil: {e}")
        # Retourne une page simplifiée sans requêtes complexes en cas d'erreur
        parfums = Parfum.objects.all()[:6]
        return render(request, 'parfums/accueil.html', {
            'parfums': parfums
        })

@cache_page(60 * 5)  # Cache pour 5 minutes
def liste_parfums(request):
    try:
        parfums = Parfum.objects.select_related('categorie').all()
        
        cache_key = 'all_categories'
        categories = cache.get(cache_key)
        if not categories:
            categories = Categorie.objects.all()
            cache.set(cache_key, categories, 3600)
        
        response = render(request, 'parfums/liste_parfums.html', {
            'parfums': parfums, 
            'categories': categories
        })
        patch_response_headers(response, cache_timeout=60 * 5)
        return response
    except Exception as e:
        print(f"Erreur sur la liste des parfums: {e}")
        parfums = Parfum.objects.all()
        categories = Categorie.objects.all()
        return render(request, 'parfums/liste_parfums.html', {
            'parfums': parfums, 
            'categories': categories
        })

@cache_page(60 * 30)  # Cache pour 30 minutes
def detail_parfum(request, parfum_id):
    try:
        cache_key = f'parfum_detail_{parfum_id}'
        parfum = cache.get(cache_key)
        
        if not parfum:
            parfum = get_object_or_404(Parfum.objects.select_related('categorie'), id=parfum_id)
            cache.set(cache_key, parfum, 60 * 30)  # 30 minutes
        
        # Vérification si l'URL utilisée est canonique (avec le slug)
        # Si ce n'est pas le cas, rediriger vers l'URL canonique
        if parfum.slug and request.path != reverse('parfums:detail_parfum_slug', kwargs={'slug': parfum.slug}):
            return redirect('parfums:detail_parfum_slug', slug=parfum.slug, permanent=True)
        
        # Recommandations de parfums similaires
        similar_parfums = Parfum.objects.filter(categorie=parfum.categorie).exclude(id=parfum.id)[:4]
        
        response = render(request, 'parfums/detail_parfum.html', {
            'parfum': parfum,
            'similar_parfums': similar_parfums
        })
        patch_response_headers(response, cache_timeout=60 * 30)
        return response
    except Exception as e:
        print(f"Erreur sur la page de détail du parfum: {e}")
        parfum = get_object_or_404(Parfum, id=parfum_id)
        return render(request, 'parfums/detail_parfum.html', {
            'parfum': parfum
        })

@cache_page(60 * 30)  # Cache pour 30 minutes
def detail_parfum_slug(request, slug):
    try:
        cache_key = f'parfum_detail_slug_{slug}'
        parfum = cache.get(cache_key)
        
        if not parfum:
            parfum = get_object_or_404(Parfum.objects.select_related('categorie'), slug=slug)
            cache.set(cache_key, parfum, 60 * 30)  # 30 minutes
        
        # Recommandations de parfums similaires
        similar_parfums = Parfum.objects.filter(categorie=parfum.categorie).exclude(id=parfum.id)[:4]
        
        response = render(request, 'parfums/detail_parfum.html', {
            'parfum': parfum,
            'similar_parfums': similar_parfums
        })
        patch_response_headers(response, cache_timeout=60 * 30)
        return response
    except Exception as e:
        print(f"Erreur sur la page de détail du parfum (slug): {e}")
        parfum = get_object_or_404(Parfum, slug=slug)
        return render(request, 'parfums/detail_parfum.html', {
            'parfum': parfum
        })

@cache_page(60 * 5)  # Cache pour 5 minutes
def parfums_par_categorie(request, categorie_id):
    try:
        cache_key = f'categorie_{categorie_id}'
        cached_data = cache.get(cache_key)
        
        if not cached_data:
            categorie = get_object_or_404(Categorie, id=categorie_id)
            
            # Vérification si l'URL utilisée est canonique (avec le slug)
            if categorie.slug and request.path != reverse('parfums:parfums_par_categorie_slug', kwargs={'slug': categorie.slug}):
                return redirect('parfums:parfums_par_categorie_slug', slug=categorie.slug, permanent=True)
            
            parfums = Parfum.objects.filter(categorie=categorie).select_related('categorie')
            categories = Categorie.objects.all()
            cached_data = {
                'categorie': categorie,
                'parfums': parfums,
                'categories': categories
            }
            cache.set(cache_key, cached_data, 60 * 5)  # 5 minutes
        
        response = render(request, 'parfums/liste_parfums.html', {
            'parfums': cached_data['parfums'], 
            'categorie_active': cached_data['categorie'],
            'categories': cached_data['categories']
        })
        patch_response_headers(response, cache_timeout=60 * 5)
        return response
    except Exception as e:
        print(f"Erreur sur la page de catégorie: {e}")
        categorie = get_object_or_404(Categorie, id=categorie_id)
        parfums = Parfum.objects.filter(categorie=categorie)
        categories = Categorie.objects.all()
        return render(request, 'parfums/liste_parfums.html', {
            'parfums': parfums, 
            'categorie_active': categorie,
            'categories': categories
        })

@cache_page(60 * 5)  # Cache pour 5 minutes
def parfums_par_categorie_slug(request, slug):
    try:
        cache_key = f'categorie_slug_{slug}'
        cached_data = cache.get(cache_key)
        
        if not cached_data:
            categorie = get_object_or_404(Categorie, slug=slug)
            parfums = Parfum.objects.filter(categorie=categorie).select_related('categorie')
            categories = Categorie.objects.all()
            cached_data = {
                'categorie': categorie,
                'parfums': parfums,
                'categories': categories
            }
            cache.set(cache_key, cached_data, 60 * 5)  # 5 minutes
        
        response = render(request, 'parfums/liste_parfums.html', {
            'parfums': cached_data['parfums'], 
            'categorie_active': cached_data['categorie'],
            'categories': cached_data['categories']
        })
        patch_response_headers(response, cache_timeout=60 * 5)
        return response
    except Exception as e:
        print(f"Erreur sur la page de catégorie (slug): {e}")
        categorie = get_object_or_404(Categorie, slug=slug)
        parfums = Parfum.objects.filter(categorie=categorie)
        categories = Categorie.objects.all()
        return render(request, 'parfums/liste_parfums.html', {
            'parfums': parfums, 
            'categorie_active': categorie,
            'categories': categories
        })

def redirect_to_canonical_parfum_url(request, parfum_id):
    """Redirection pour les anciennes URLs vers les nouvelles avec slug (pour le SEO)"""
    parfum = get_object_or_404(Parfum, id=parfum_id)
    if parfum.slug:
        return redirect('parfums:detail_parfum_slug', slug=parfum.slug, permanent=True)
    return redirect('parfums:detail_parfum', parfum_id=parfum_id)

@cache_page(60 * 60 * 24)  # Cache pour 24 heures
def sitemap_view(request):
    """Génération d'un sitemap XML simple pour les moteurs de recherche"""
    parfums = Parfum.objects.all()
    categories = Categorie.objects.all()
    
    return render(request, 'parfums/sitemap.xml', {
        'parfums': parfums,
        'categories': categories,
        'domain': request.get_host()
    }, content_type='application/xml')

@cache_page(60 * 60 * 24)  # Cache pour 24 heures
def robots_txt(request):
    """Génération du fichier robots.txt"""
    return HttpResponse("""User-agent: *
Allow: /
Sitemap: {}://{}/sitemap.xml
""".format(request.scheme, request.get_host()), content_type="text/plain")

def trigger_error(request):
    division_by_zero = 1 / 0
    return HttpResponseServerError("An error occurred.")
