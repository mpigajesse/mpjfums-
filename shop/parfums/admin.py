from django.contrib import admin
from .models import Categorie, Parfum

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)

@admin.register(Parfum)
class ParfumAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix', 'stock', 'date_ajout')
    list_filter = ('categorie', 'date_ajout')
    search_fields = ('nom', 'description')
    readonly_fields = ('date_ajout',)
    list_editable = ('prix', 'stock')
    list_per_page = 20
