from cotlette.apps import AppConfig


class AdminConfig(AppConfig):
    default_auto_field = 'cotlette.db.models.BigAutoField'
    name = 'apps.users'
