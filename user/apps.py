from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    # def ready(self):
    #     import user.signals  # 导入信号文件