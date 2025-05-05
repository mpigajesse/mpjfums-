from django.test import TestCase, Client
from .models import Categorie, Parfum
from django.urls import reverse

class CategorieModelTest(TestCase):
    def test_categorie_creation(self):
        categorie = Categorie.objects.create(nom="Parfums pour homme", description="Des fragrances masculines")
        self.assertEqual(categorie.nom, "Parfums pour homme")
        self.assertTrue(Categorie.objects.exists())

class ParfumModelTest(TestCase):
    def setUp(self):
        self.categorie = Categorie.objects.create(nom="Parfums pour femme", description="Des fragrances féminines")
        
    def test_parfum_creation(self):
        parfum = Parfum.objects.create(
            nom="Rose Élégante",
            description="Un parfum floral avec des notes de rose et de jasmin",
            prix=89.99,
            stock=15,
            image="https://example.com/rose.jpg",
            categorie=self.categorie
        )
        self.assertEqual(parfum.nom, "Rose Élégante")
        self.assertEqual(parfum.prix, 89.99)
        self.assertEqual(parfum.categorie, self.categorie)
        self.assertTrue(Parfum.objects.exists())

class ViewsTest(TestCase):
    def setUp(self):
        self.categorie = Categorie.objects.create(
            nom="Parfums unisexe", 
            description="Des fragrances pour tous",
            slug="parfums-unisexe"
        )
        self.parfum = Parfum.objects.create(
            nom="Ocean Breeze",
            description="Un parfum frais avec des notes marines",
            prix=69.99,
            stock=10,
            categorie=self.categorie,
            slug="ocean-breeze"
        )
        
    def test_accueil_view(self):
        response = self.client.get(reverse('parfums:accueil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parfums/accueil.html')
        self.assertContains(response, "MPJFUMS")
        
    def test_liste_parfums_view(self):
        response = self.client.get(reverse('parfums:liste_parfums'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parfums/liste_parfums.html')
        self.assertContains(response, "Ocean Breeze")
        
    def test_detail_parfum_view(self):
        # Utilisation directe de l'URL avec slug qui ne génère pas de redirection
        response = self.client.get(reverse('parfums:detail_parfum_slug', args=[self.parfum.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parfums/detail_parfum.html')
        self.assertContains(response, "Ocean Breeze")
        
        # Ancienne URL qui devrait rediriger (code 301)
        old_url_response = self.client.get(reverse('parfums:detail_parfum', args=[self.parfum.id]))
        self.assertEqual(old_url_response.status_code, 301)
        
    def test_parfums_par_categorie_view(self):
        # Utilisation directe de l'URL avec slug qui ne génère pas de redirection
        response = self.client.get(reverse('parfums:parfums_par_categorie_slug', args=[self.categorie.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parfums/liste_parfums.html')
        self.assertContains(response, "Parfums unisexe")
        
        # Ancienne URL qui devrait rediriger (code 301)
        old_url_response = self.client.get(reverse('parfums:parfums_par_categorie', args=[self.categorie.id]))
        self.assertEqual(old_url_response.status_code, 301)

class BasicViewsTest(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.client = Client()
    
    def test_accueil_view_status(self):
        # Test that the accueil view returns a 200 OK status
        response = self.client.get(reverse('parfums:accueil'))
        self.assertEqual(response.status_code, 200)
        
    def test_liste_parfums_view_status(self):
        # Test that the liste_parfums view returns a 200 OK status
        response = self.client.get(reverse('parfums:liste_parfums'))
        self.assertEqual(response.status_code, 200)
