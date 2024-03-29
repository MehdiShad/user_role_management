from . import monkey_patch_user, monkey_patch_group
from django.apps import AppConfig
from user_role_management.guardian.conf import settings


class GuardianConfig(AppConfig):
    name = 'user_role_management.guardian'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        # Must patch Company_group here since generic
        # group permission model is definable
        monkey_patch_group()
        if settings.MONKEY_PATCH:
            monkey_patch_user()
