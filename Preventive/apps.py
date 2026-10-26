from django.apps import AppConfig


class PreventiveConfig(AppConfig):
    name = 'Preventive'

    def ready(self):
        import Preventive.PreventiveSignal
