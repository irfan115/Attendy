from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser

TEACHER = 0
ADMIN = 1

class AuthUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, is_active, user_role=TEACHER, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError(
                _('Email is required to create user'))
        email = self.normalize_email(email)
        """
        user = self.model(email=email, user_role=user_role, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        """

        user = self.model(email=email,
                          is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, user_role=user_role, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, user_role=TEACHER, **extra_fields):
        return self._create_user(email, password, False, False, False, user_role=user_role, **extra_fields)

    def create_superuser(self, email, password, user_role=ADMIN, **extra_fields):
        return self._create_user(email, password, is_staff=True, is_superuser=True,
                                 is_active=True, user_role=user_role, **extra_fields)


class Teacher(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(
        verbose_name=_("Last Name"), max_length=50)
    email = models.EmailField(
        verbose_name=_("Email"), unique=True, max_length=255)

    is_staff = models.BooleanField(
        verbose_name=_('staff'), default=False, null=False)
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as ' 'active. '
                                                                           'Unselect this instead of deleting accounts.'))

    TEACHER = 0
    ADMIN = 1

    USER_ROLES = (
        (TEACHER, _('TEACHER')),
        (ADMIN, _('Admin'))
    )
    user_role = models.PositiveSmallIntegerField(verbose_name=_("User Role"), choices=USER_ROLES, default=TEACHER,
                                                 blank=False, null=False, max_length=10)
    objects = AuthUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        name = '%s %s' % self.first_name, self.last_name
        return name

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
            return '%s %s' % (self.first_name, self.last_name)


