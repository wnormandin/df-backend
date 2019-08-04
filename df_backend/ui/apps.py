from django.apps import AppConfig


class UiConfig(AppConfig):
    name = 'ui'

    def ready(self):
        from ..utils import setup_logging
        setup_logging()
