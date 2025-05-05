from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.conf.urls.static import static

# Vues spéciales pour les fichiers statiques avec cache long
@cache_control(max_age=2592000)  # 30 jours de cache
def serve_robots_txt(request):
    return serve(request, 'robots.txt', document_root=settings.STATIC_ROOT)

@cache_control(max_age=2592000)  # 30 jours de cache
def serve_manifest_json(request):
    return serve(request, 'manifest.json', document_root=settings.STATIC_ROOT)

# Vue personnalisée pour les erreurs 404
def page_not_found(request, exception):
    return TemplateView.as_view(template_name='parfums/404.html')(request)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/parfums/', include('parfums.urls')),
    path('', RedirectView.as_view(url='/shop/parfums/')),  # Redirection de la racine vers /shop/parfums/
    
    # Fichiers spéciaux pour SEO et PWA
    path('robots.txt', serve_robots_txt),
    path('manifest.json', serve_manifest_json),
    
    # Page d'erreur 404 personnalisée pour test
    path('404/', TemplateView.as_view(template_name='parfums/404.html'), name='page_404'),
    
    # Django Browser Reload pour le développement
    path("__reload__/", include("django_browser_reload.urls")),
]

# Ajout du handler404 personnalisé
handler404 = 'shop.urls.page_not_found'

# Ajouter les URLs de DEBUG uniquement en développement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
