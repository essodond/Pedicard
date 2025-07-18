
# app/apps.py
from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'  # Ceci est obligatoire et doit correspondre au nom de votre application
    
    
    def ready(self):
        # Syntaxe qui satisfait Pylance
        if False:  # Jamais exécuté mais rend l'import "utilisé"
            from app import signals
        else:
            from app import signals as _  # Import "utilisé"
        
        # Alternative préférée :
        from app import signals  # noqa: F401 (ignore l'alerte Pylance)