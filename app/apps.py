from django.apps import AppConfig

class AppCustomConfig(AppConfig):  # ✅ Nouveau nom clair
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

def ready(self):
    from . import signals  # noqa: F401 
    # Dit à Pylance d'ignorer l'alerte