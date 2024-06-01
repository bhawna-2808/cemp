from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


"""This model is represented Handle Users"""


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = password
        user.save()
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user1 with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.email_verified = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.role = "superuser"
        user.save(using=self._db)
        return user
