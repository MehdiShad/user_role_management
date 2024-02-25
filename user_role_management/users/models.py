from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from user_role_management.common.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager as BUM, PermissionsMixin, Group, GroupManager, Permission


class UserTypesChoices(models.TextChoices):
    STAFF = '1', 'staff'
    CUSTOMER = '2', 'customer'
    SUPERVISOR = '3', 'supervisor'


class BaseUserManager(BUM):
    def create_user(self, email, is_active=True, is_admin=False, password=None, is_staff=False):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email.lower()), is_active=is_active, is_admin=is_admin, is_staff=is_staff)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            is_staff=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


# class PermissionsMixin(BM):
#     groups = models.ManyToManyField(
#         BaseGroup,
#         verbose_name=_("groups"),
#         blank=True,
#         help_text=_(
#             "The groups this user belongs to. A user will get all permissions "
#             "granted to each of their groups."
#         ),
#         related_name="user_set",
#         related_query_name="user",
#     )

class Company(BaseModel):
    title = models.CharField(max_length=155)
    users = models.ManyToManyField('BaseUser')

    def __str__(self):
        return str(self.title)


class CompanyGroups(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, null=True, blank=True)

    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
    )

    class Meta:
        verbose_name = _("company group")
        verbose_name_plural = _("company groups")

    def __str__(self):
        return f"{self.company} - {self.group}"

    def save(self, *args, **kwargs):
        self.name = self.name if self.name else f"{self.company.title}_{self.group.name}"

        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.company,)


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name="email address", unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=UserTypesChoices.choices, default='2')
    is_staff = models.BooleanField(default=False)
    last_company_logged_in = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    company_groups = models.ManyToManyField(
        CompanyGroups,
        verbose_name=_("company_groups"),
        blank=True,
        help_text=_(
            "The company_groups this user belongs to. A user will get all permissions "
            "granted to each of their company_groups."
        ),
        related_name="base_user_set",
        related_query_name="base_user",
    )

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email


class Assigned_customer(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING, related_name='user')
    customer = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING, related_name='customer')

    def __str__(self):
        return f"{self.user.email}: {self.customer.email}"


class Employee(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    personnel_code = models.CharField(max_length=15)
    user = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = [
            ('company', 'user'),
            ('user', 'personnel_code'),
            ('company', 'personnel_code'),
            ('user', 'company', 'personnel_code')
        ]

    def __str__(self):
        return f"{self.company.title}-{self.user.email}"


class Position(models.Model):
    title = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=55, null=True, blank=True)
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return str(self.title)


class Department(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return str(self.title)


class Company_departments(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name='department')
    parent_department = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='parent_company_department')
    manager = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ['company', 'department']

    def __str__(self):
        return f"{self.company.title}-{self.department.title}"


class Company_departments_employees(models.Model):
    company_departments = models.ForeignKey(Company_departments, on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='employee')
    supervisor = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='supervisor')

    class Meta:
        unique_together = ['company_departments', 'employee']

    def __str__(self):
        return f"{self.company_departments}-{self.employee.user.email}"


class Company_branches(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    branch_title = models.CharField(max_length=255)
    branch_manager = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='branch_manager')
    employees = models.ManyToManyField(Employee)

    class Meta:
        unique_together = ['company', 'branch_title']

    def __str__(self):
        return f"{self.company.title}-{self.branch_title}"


class Shift(BaseModel):
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    created_by = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING)
    # company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    companies = models.ManyToManyField(Company)
    employees = models.ManyToManyField(Employee)

    class Meta:
        unique_together = ['started_at', 'ended_at']


    def __str__(self):
        return f"{self.started_at}-{self.ended_at}"


class Process(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['company', 'name']
        permissions = [('dg_can_view_process', 'OBP can view process'), ('dg_can_start_process', 'OBP can start process')]

    def __str__(self):
        return str(self.name)


class Route(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        permissions = [('dg_can_get_route', 'OBP can get route'), ('dg_can_post_route', 'OBP can post route')]

    def __str__(self):
        return str(self.name)


# class CustomPermission(models.Model):
#     description = models.CharField(max_length=255)
#     company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
#     groups = models.ForeignKey(Group, on_delete=models.DO_NOTHING)

