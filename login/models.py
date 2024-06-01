from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from .manager import CustomUserManager


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value



class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(_("name"), max_length=150)
    email = models.EmailField(unique=True, null=True, blank=True)
    mobile_number = models.CharField(
        _("Mobile Number"), max_length=12, unique=True, null=True, blank=True
    )
    password = models.CharField(max_length=12)
    otp = models.CharField(max_length=7, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(_("Active"), default=True)
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # Use the 'email' field for authentication
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if len(self.password) < 20:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email if self.email else self.mobile_number

    



