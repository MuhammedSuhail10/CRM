from django.apps import AppConfig

class CrmuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crmuser'
    
    def ready(self):
        import crmuser.signals