from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"
    verbose_name = "Core"

    def ready(self):
        # Imports anything from `.signals` to run the whole module.
        from .signals import send_to_slack  # noqa: F401
