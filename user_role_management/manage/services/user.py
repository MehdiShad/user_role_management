from typing import Dict, Literal
from django.db import transaction
from django.http import HttpRequest
from user_role_management.manage.models import BaseUser, Process
from user_role_management.core.exceptions import error_response, success_response
from django.contrib.auth.decorators import login_required, permission_required
from user_role_management.manage import model_choices


def create_customer(*, email: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(email=email, password=password, type=model_choices.UserTypesChoices.CUSTOMER)


def create_employee(*, email: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(email=email, password=password, type=model_choices.UserTypesChoices.STAFF)


@transaction.atomic
def register(*, email: str, password: str) -> BaseUser:
    user = create_customer(email=email, password=password)
    return user


def update_user(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    # TODO: Add companies to update the user
    return BaseUser._update(id=id, **kwargs)
