from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'parfums'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('parfums/', views.liste_parfums, name='liste_parfums'),
    
    # Nouvelles URLs avec slug (SEO-friendly)
    path('parfum/<slug:slug>/', views.detail_parfum_slug, name='detail_parfum_slug'),
    path('categorie/<slug:slug>/', views.parfums_par_categorie_slug, name='parfums_par_categorie_slug'),
    
    # URLs originales (pour la compatibilité)
    path('parfums/<int:parfum_id>/', views.detail_parfum, name='detail_parfum'),
    path('categories/<int:categorie_id>/', views.parfums_par_categorie, name='parfums_par_categorie'),
    
    # Redirection pour améliorer le référencement
    path('parfums/detail/<int:parfum_id>/', views.redirect_to_canonical_parfum_url, name='old_detail_parfum'),
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    
    # Sentry pour la surveillance des erreurs
    path('sentry-debug/', views.trigger_error, name='sentry_debug'),
    
    # Page d'erreur 404 pour test
    path('404/', TemplateView.as_view(template_name='404.html'), name='page_404_test'),
] 