import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators 
from django.utils.deconstruct import deconstructible

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _normalize_mobile_number(self, mobile_number):
        return mobile_number
    
    def _create_user(self, mobile_number, password, **extra_fields):
        if not mobile_number:
            raise ValueError('The given username must be set')
        # email = self.normalize_email(email)
        mobile_number = self._normalize_mobile_number(mobile_number)
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_user(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile_number, password, **extra_fields)
    
    def create_superuser(self, mobile_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(mobile_number, password, **extra_fields)
    
    
@deconstructible
class UnicodeMobileNumberValidator(validators.RegexValidator):
    regex = r'09(\d{9})$'
    message = _(
        'Enter a valid mobile number. This value may contain only numbers.'
    )
    flags = 0
    
class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User Model support using mobile instead of usename """
    mobile_number_validator = UnicodeMobileNumberValidator()
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    username = models.CharField(
        verbose_name=_('username'),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    )
    mobile_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Mobile Number'),
        validators=[mobile_number_validator],
        error_messages={
         'unique': _("A user with that mobile number already exists."),
        }
    )
    first_name = models.CharField(max_length=255,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    email = models.EmailField(max_length=255,unique=True,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)# Simplest possible answer: All admins are staff
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "mobile_number" ## to change default username field to mobile field
    
    