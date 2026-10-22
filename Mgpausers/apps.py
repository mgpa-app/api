from django.apps import AppConfig


class MgpausersConfig(AppConfig):
    name = 'Mgpausers'

    def ready(self):
        import Mgpausers.MgpauserSignal
