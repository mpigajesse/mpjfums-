from django.conf import settings

def debug(request):
    """
    Ajoute la variable DEBUG de settings au contexte des templates
    Cela permet d'inclure certains éléments seulement en mode développement
    """
    return {'debug': settings.DEBUG} 