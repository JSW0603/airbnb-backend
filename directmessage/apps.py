from django.apps import AppConfig


class DirectmessageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "directmessage"
    verbose_name = "Direct Messages" #directmessages에서 이름 변경