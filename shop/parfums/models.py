from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.cache import cache
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Categorie(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, help_text="Description pour les moteurs de recherche (max 160 caractères)")
    
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('parfums:parfums_par_categorie', args=[str(self.id)])
    
    def get_parfums_count(self):
        # Mise en cache du nombre de parfums par catégorie
        cache_key = f'categorie_parfums_count_{self.id}'
        count = cache.get(cache_key)
        if count is None:
            count = self.parfums.count()
            cache.set(cache_key, count, 3600)  # Cache pour 1 heure
        return count

class Parfum(models.Model):
    nom = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    description = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True, help_text="Description pour les moteurs de recherche (max 160 caractères)")
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.CharField(max_length=255, blank=True)  # URL de l'image externe (Unsplash)
    image_thumbnail = ImageSpecField(source='image_locale',
                                     processors=[ResizeToFill(300, 300)],
                                     format='JPEG',
                                     options={'quality': 85})
    image_large = ImageSpecField(source='image_locale',
                                processors=[ResizeToFill(1200, 800)],
                                format='JPEG',
                                options={'quality': 90})
    image_locale = models.ImageField(upload_to='parfums/', blank=True, null=True)
    image_alt = models.CharField(max_length=100, blank=True, help_text="Texte alternatif pour l'image (important pour le SEO)")
    categorie = models.ForeignKey(Categorie, related_name='parfums', on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)  # Pour les parfums mis en avant
    
    # Attributs supplémentaires pour améliorer le référencement
    notes_de_tete = models.CharField(max_length=255, blank=True, help_text="Notes de tête du parfum")
    notes_de_coeur = models.CharField(max_length=255, blank=True, help_text="Notes de coeur du parfum")
    notes_de_fond = models.CharField(max_length=255, blank=True, help_text="Notes de fond du parfum")
    
    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return reverse('parfums:detail_parfum', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        
        # Génère automatiquement une meta-description si celle-ci n'est pas fournie
        if not self.meta_description and self.description:
            # Limite à 157 caractères pour ajouter "..." à la fin
            self.meta_description = self.description[:157] + "..." if len(self.description) > 160 else self.description
            
        # S'assurer que l'image a un texte alternatif pour l'accessibilité
        if not self.image_alt and self.nom:
            self.image_alt = f"Parfum {self.nom}"
        
        # Invalider le cache lorsqu'un parfum est modifié
        cache_key = f'categorie_parfums_count_{self.categorie_id}'
        cache.delete(cache_key)
        cache_key = f'parfum_detail_{self.id}'
        cache.delete(cache_key)
        
        super().save(*args, **kwargs)
    
    def get_display_image(self):
        """Retourne l'URL d'image à afficher, priorisant l'image locale si disponible."""
        if self.image_locale and hasattr(self.image_thumbnail, 'url'):
            return self.image_thumbnail.url
        return self.image
        
    def get_notes_details(self):
        """Retourne un dictionnaire des notes de parfum pour affichage structuré"""
        notes = {}
        if self.notes_de_tete:
            notes['tete'] = self.notes_de_tete
        if self.notes_de_coeur:
            notes['coeur'] = self.notes_de_coeur
        if self.notes_de_fond:
            notes['fond'] = self.notes_de_fond
        return notes
