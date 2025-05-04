from django.db import models

# Create your models here.

class Categorie(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.nom

class Parfum(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.CharField(max_length=255, blank=True)  # URL de l'image
    categorie = models.ForeignKey(Categorie, related_name='parfums', on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nom
