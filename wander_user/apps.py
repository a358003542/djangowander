from django.apps import AppConfig


class WanderUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wander_user'

    def ready(self):
        # 注册信号
        import wander_user.signals