from django.apps import AppConfig

app_name = 'base'

class BaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "base"
