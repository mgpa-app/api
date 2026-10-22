from django.apps import AppConfig


class MatroulantConfig(AppConfig):
    name = 'Matroulant'

    def ready(self):
        import Matroulant.MatroulantSignal
