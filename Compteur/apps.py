from django.apps import AppConfig


class CompteurConfig(AppConfig):
    name = 'Compteur'

    def ready(self):
        import Compteur.CompteurSignal
