from django.db import models
from django.db.models import QuerySet
from typing import Dict, Any, Optional, Literal
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from user_role_management.common.models import BaseModel
from user_role_management.utils.services import create_fields
from user_role_management.core.exceptions import error_response, success_response
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager as BUM, PermissionsMixin, Group, GroupManager, \
    Permission
from user_role_management.manage import model_choices


def validate_user_type(value):
    if value not in [choice[0] for choice in model_choices.UserTypesChoices.choices]:
        raise ValidationError(f"'{value}' is not a valid user type")


def validate_last_company_logged_in(value):
    """
        Verify matching users and companies.
    """
    # TODO: Verify matching users and companies.
    pass


class BaseUserManager(BUM):
    def create_user(self, email, is_active=True, is_admin=False, password=None, is_staff=False, type='2'):
        if not email:
            raise ValueError("manage must have an email address")

        user = self.model(email=self.normalize_email(email.lower()), is_active=is_active, is_admin=is_admin,
                          is_staff=is_staff, type=type)

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


class Company(BaseModel):
    title = models.CharField(max_length=155, unique=True)

    # users = models.ManyToManyField('BaseUser', related_name='users')

    class Meta:
        verbose_name = _("company")
        verbose_name_plural = _("companies")

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
    def _get_all(cls) -> QuerySet['Company']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['Comapny']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    @classmethod
    def __str__(self):
        return str(self.title)


class Company_group(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, null=True, blank=True)

    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
    )

    class Meta:
        unique_together = ['company', 'group']
        verbose_name = _("company group")
        verbose_name_plural = _("company groups")

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
    def _get_all(cls) -> QuerySet['Company_group']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['Company_group']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    def __str__(self):
        return f"{self.company} - {self.group}"

    def save(self, *args, **kwargs):
        self.name = f"{self.company.title}_{self.group.name}"

        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.company,)


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address", unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    type = models.CharField(max_length=2, choices=model_choices.UserTypesChoices.choices, default='2',
                            validators=[validate_user_type])
    is_staff = models.BooleanField(default=False)
    last_company_logged_in = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True,
                                               validators=[validate_last_company_logged_in])
    company_groups = models.ManyToManyField(
        Company_group,
        verbose_name=_("company_groups"),
        blank=True,
        help_text=_(
            "The company_group this user belongs to. A user will get all permissions "
            "granted to each of their company_group."
        ),
        related_name="base_user_set",
        related_query_name="base_user",
    )
    companies = models.ManyToManyField('Company', blank=True, related_name='companies')

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

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
            obj.full_clean()
            obj.save()
            return success_response(data=obj)
        # except ValidationError as ve:
        #     sdf = ''
        except Exception as ex:
            return error_response(message=str(ex))

    @classmethod
    def _get_all(cls) -> QuerySet['BaseUser']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['BaseUser']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    @classmethod
    def filtered_by_company(cls, company: Company) -> QuerySet['BaseUser']:
        return cls.objects.filter(companies=company)

    def __str__(self):
        return self.email


class Assigned_customer(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING, related_name='user')
    customer = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING, related_name='customer')

    class Meta:
        verbose_name = _("assigned customer")
        verbose_name_plural = _("assigned customers")

    def __str__(self):
        return f"{self.user.email}: {self.customer.email}"


class Company_position(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=55, null=True, blank=True)

    class Meta:
        verbose_name = _("Company position")
        verbose_name_plural = _("Company Positions")

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
    def _get_all(cls) -> QuerySet['Company_position']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['Company_position']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    @classmethod
    def filtered_by_company(cls, company: Company) -> QuerySet['Company_position']:
        company_id = company.id if company else None
        return cls.objects.filter(company_id=company_id)

    def __str__(self):
        return str(self.title)


class Employee(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    personnel_code = models.CharField(max_length=45)
    user = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING)
    positions = models.ManyToManyField(Company_position)

    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")
        unique_together = [
            ('company', 'user'),
            ('user', 'personnel_code'),
            ('company', 'personnel_code'),
            ('user', 'company', 'personnel_code')
        ]

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
    def _get_all(cls) -> QuerySet['Employee']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['Employee']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    @classmethod
    def filtered_by_company(cls, company: Company) -> QuerySet['Company_position']:
        company_id = company.id if company else None
        return cls.objects.filter(company_id=company_id)

    def __str__(self):
        return f"{self.company.title}-{self.user.email}"


class Company_department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    department = models.CharField(max_length=255)
    parent_department = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True,
                                          related_name='parent_company_department')
    manager = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        unique_together = ['company', 'department']
        verbose_name = _("company department")
        verbose_name_plural = _("company departments")

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
    def _get_all(cls) -> QuerySet['Company_department']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['Company_department']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    @classmethod
    def filtered_by_company(cls, company: Company) -> QuerySet['Company_position']:
        company_id = company.id if company else None
        return cls.objects.filter(company_id=company_id)

    def __str__(self):
        return f"{self.company.title}-{self.department}"


class Company_department_employee(models.Model):
    company_department = models.ForeignKey(Company_department, on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='employee')
    supervisor = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='supervisor', null=True,
                                   blank=True)

    class Meta:
        verbose_name = _("company department employee")
        verbose_name_plural = _("company department employees")
        unique_together = ['company_department', 'employee']

    @classmethod
    def _create(cls, **kwargs: Dict[str, Any]) -> Dict[str, Literal['is_success', True, False]]:
        try:
            fields = create_fields(**kwargs)
            new = cls.objects.create(**fields)
            # TODO: Hanle django.db.utils.IntegrityError: insert or update on table "manage_company_department_employee" violates foreign key constraint "manage_company_depar_employee_id_c569378a_fk_manage_em"
            # DETAIL:  Key (employee_id)=(8) is not present in table "manage_employee".
            new.full_clean()
            response = success_response(data=new)
            return response
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
    def _get_all(cls) -> QuerySet['Company_department_employee']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['Company_department_employee']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    @classmethod
    def filtered_by_company(cls, company: Company) -> QuerySet['Company_department_employee']:
        company_id = company.id if company else None
        return cls.objects.filter(company_department__company_id=company_id)

    def __str__(self):
        return f"{self.company_department}-{self.employee.user.email}"


class Company_department_position(models.Model):
    company_department = models.ForeignKey(Company_department, on_delete=models.DO_NOTHING)
    company_position = models.ForeignKey(Company_position, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ['company_department', 'company_position']
        verbose_name = _("company department position")
        verbose_name_plural = _("company department positions")

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
    def _get_all(cls) -> QuerySet['Company_department_position']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['Company_department_position']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    def filtered_by_company(cls, company: Company) -> QuerySet['Company_department_position']:
        company_id = company.id if company else None
        return cls.objects.filter(company_department__company_id=company_id)

    def __str__(self):
        return f"{self.company_department.department}-{self.company_position.title}"


class Company_branch(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    branch_title = models.CharField(max_length=255)
    branch_manager = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='branch_manager')
    employees = models.ManyToManyField(Employee)

    class Meta:
        verbose_name = _("company branch")
        verbose_name_plural = _("company branches")
        unique_together = ['company', 'branch_title']

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
    def _get_all(cls) -> QuerySet['Company_branch']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['Company_branch']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

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
    def _get_all(cls) -> QuerySet['Shift']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['Shift']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    def __str__(self):
        return f"{self.started_at}-{self.ended_at}"


class Process(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("process")
        verbose_name_plural = _("processes")
        unique_together = ['company', 'name']
        permissions = [('dg_can_view_process', 'OBP can view process'),
                       ('dg_can_start_process', 'OBP can start process')]

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
    def _get_all(cls) -> QuerySet['Process']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['Process']:
        try:
            return cls.objects.get(id=id)
        except:
            return None

    @classmethod
    def filtered_by_company(cls, company: Company) -> QuerySet['Process']:
        company_id = company.id if company else None
        return cls.objects.filter(company_id=company_id)

    def __str__(self):
        return f"{self.company}_{self.name}"


class Action(models.Model):
    process = models.ForeignKey(Process, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=355)
    code_name = models.CharField(max_length=255)
    route = models.CharField(max_length=355, null=True, blank=True)

    class Meta:
        unique_together = ['process', 'code_name']
        permissions = [('dg_can_do_this_action', 'OBP can do this action')]

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
    def _get_all(cls) -> QuerySet['Action']:
        return cls.objects.all()

    @classmethod
    def _get_by_id(cls, id: int) -> Optional['Action']:
        try:
            return cls.objects.get(id=id)
        except:
            return None
    
    
    @classmethod
    def filtered_by_company(cls, company: Company) -> QuerySet['Action']:
        company_id = company.id if company else None
        return cls.objects.filter(process__company_id=company_id)

    def __str__(self):
        return f"{self.process}_{self.name}"


# class CustomPermission(models.Model):
#     description = models.CharField(max_length=255)
#     company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
#     groups = models.ForeignKey(Group, on_delete=models.DO_NOTHING)

class Order(BaseModel):
    order_total = models.IntegerField()
    customer = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=50, choices=model_choices.OrderStatusChoices.choices, default='2')

    def __str__(self):
        return f"{self.customer}: {self.order_total}"
