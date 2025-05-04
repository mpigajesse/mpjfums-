from django.urls import path
from . import views

app_name = 'parfums'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('parfums/', views.liste_parfums, name='liste_parfums'),
    path('parfums/<int:parfum_id>/', views.detail_parfum, name='detail_parfum'),
    path('categories/<int:categorie_id>/', views.parfums_par_categorie, name='parfums_par_categorie'),
] 