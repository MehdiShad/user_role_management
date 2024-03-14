from django.db import models


class UserTypesChoices(models.TextChoices):
    STAFF = '1', 'staff'
    CUSTOMER = '2', 'customer'
    SUPERVISOR = '3', 'supervisor'


class OrderStatusChoices(models.TextChoices):
    SALESQUOTATION = '1', 'Sale quotation'
    SALEORDER = '2', 'Sale order'
    INVOICE = '3', 'Invoice'