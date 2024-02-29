from django.db import models
from django.db.models import QuerySet
from typing import Dict, Any, Optional, Literal
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from user_role_management.manage.models import Company_groups
from django.contrib.contenttypes.fields import GenericForeignKey
from user_role_management.guardian.compat import user_model_label
from user_role_management.guardian.ctypes import get_content_type
from user_role_management.utils.model_handler import create_fields
from user_role_management.core.exceptions import error_response, success_response
from user_role_management.guardian.managers import GroupObjectPermissionManager, UserObjectPermissionManager


class BaseObjectPermission(models.Model):
    """
    Abstract ObjectPermission class. Actual class should additionally define
    a ``content_object`` field and either ``user`` or ``group`` field.
    """
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return '{} | {} | {}'.format(
            str(self.content_object),
            str(getattr(self, 'user', False) or self.group),
            str(self.permission.codename))

    def save(self, *args, **kwargs):
        content_type = get_content_type(self.content_object)
        if content_type != self.permission.content_type:
            raise ValidationError("Cannot persist permission not designed for "
                                  "this class (permission's type is %r and object's type is %r)"
                                  % (self.permission.content_type, content_type))
        return super().save(*args, **kwargs)


class BaseGenericObjectPermission(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.CharField(_('object ID'), max_length=255)
    content_object = GenericForeignKey(fk_field='object_pk')

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['content_type', 'object_pk']),
        ]


class UserObjectPermissionBase(BaseObjectPermission):
    """
    **Manager**: :manager:`UserObjectPermissionManager`
    """
    user = models.ForeignKey(user_model_label, on_delete=models.CASCADE)

    objects = UserObjectPermissionManager()

    class Meta:
        abstract = True
        unique_together = ['user', 'permission', 'content_object']


class UserObjectPermissionAbstract(UserObjectPermissionBase, BaseGenericObjectPermission):

    class Meta(UserObjectPermissionBase.Meta, BaseGenericObjectPermission.Meta):
        abstract = True
        unique_together = ['user', 'permission', 'object_pk']


class UserObjectPermission(UserObjectPermissionAbstract):

    class Meta(UserObjectPermissionAbstract.Meta):
        abstract = False


    @classmethod
    def _create(cls, **kwargs: Dict[str, Any]) -> Dict[str, Literal['is_success', True, False]]:
        try:
            fields = create_fields(**kwargs)
            new = cls.objects.create(**fields)
            return success_response(data=new)
        except Exception as ex:
            return error_response(message=str(ex))

    @classmethod
    def _update(cls, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
        try:
            obj = cls.objects.get(id=id)
            fields = create_fields(**kwargs)
            obj.__dict__.update(**fields)
            obj.save()
            return success_response(data=obj)
        except Exception as ex:
            return error_response(message=str(ex))

    @classmethod
    def _get_all(cls) -> QuerySet['UserObjectPermission']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['UserObjectPermission']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    # def __str__(self):
    #     return f"{self.process}_{self.title}"


class GroupObjectPermissionBase(BaseObjectPermission):
    """
    **Manager**: :manager:`GroupObjectPermissionManager`
    """
    group = models.ForeignKey(Company_groups, on_delete=models.CASCADE)

    objects = GroupObjectPermissionManager()

    class Meta:
        abstract = True
        unique_together = ['group', 'permission', 'content_object']


class GroupObjectPermissionAbstract(GroupObjectPermissionBase, BaseGenericObjectPermission):

    class Meta(GroupObjectPermissionBase.Meta, BaseGenericObjectPermission.Meta):
        abstract = True
        unique_together = ['group', 'permission', 'object_pk']

class GroupObjectPermission(GroupObjectPermissionAbstract):

    class Meta(GroupObjectPermissionAbstract.Meta):
        abstract = False

    @classmethod
    def _create(cls, **kwargs: Dict[str, Any]) -> Dict[str, Literal['is_success', True, False]]:
        try:
            fields = create_fields(**kwargs)
            new = cls.objects.create(**fields)
            return success_response(data=new)
        except Exception as ex:
            return error_response(message=str(ex))

    @classmethod
    def _update(cls, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
        try:
            obj = cls.objects.get(id=id)
            fields = create_fields(**kwargs)
            obj.__dict__.update(**fields)
            obj.save()
            return success_response(data=obj)
        except Exception as ex:
            return error_response(message=str(ex))

    @classmethod
    def _get_all(cls) -> QuerySet['GroupObjectPermission']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['GroupObjectPermission']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    # def __str__(self):
    #     return f"{self.process}_{self.title}"
