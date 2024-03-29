from rest_framework import serializers
from django.core.exceptions import ValidationError


def create_fields(**kwargs):
    fields = {}
    for key, value in kwargs.items():
        if value is not None:
            fields[key] = value
    return fields
