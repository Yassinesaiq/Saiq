from django.apps import AppConfig


class BusManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BusManagement_App'


class VotreAppConfig(AppConfig):
    name = 'BusManagement_App'

    def ready(self):
        import BusManagement_App.signals
