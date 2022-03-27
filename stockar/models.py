import uuid
from decimal import Decimal

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not first_name:
            raise ValueError('Users must have a first name')

        if not last_name:
            raise ValueError('Users must have a last name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=200, blank=True, null=True)

    objects = AccountManager()

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Email & Password are required by default.

    def get_full_name(self):
        return f'{self.first_name} {self.last_name} - {self.email}'

    def get_short_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class StorageOffer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255, blank=False, null=False)
    description = models.TextField(max_length=1024, blank=False, null=False)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, null=False,
                                        validators=[MinValueValidator(Decimal('0.01'))])
    active = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StorageSpace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255, blank=False, null=False)
    width = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))],
                                null=True, blank=True)
    depth = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))],
                                null=True, blank=True)
    storage_offer = models.ForeignKey(StorageOffer, on_delete=models.CASCADE, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AccessCode(models.Model):
    alphanumeric = RegexValidator(r'^[0-9AB]*$', 'Only numeric, A and B characters are allowed.')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(unique=True, blank=False, null=False, max_length=255, validators=[alphanumeric])
    added_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
