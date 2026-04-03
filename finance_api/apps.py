from django.apps import AppConfig


class FinanceApiConfig(AppConfig):
    name = 'finance_api'

    def ready(self):
        # register signals
        import finance_api.signals  # noqa: F401
