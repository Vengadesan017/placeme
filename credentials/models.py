from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile_no, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not mobile_no:
            raise ValueError('The Mobile number must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, mobile_no=mobile_no, **extra_fields)
        user.set_password(password)
        user.joineddatetime = timezone.now()
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, mobile_no, password=None, **extra_fields):
    #     extra_fields.setdefault('is_admin', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     return self.create_user(email, mobile_no, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    userid = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    joined_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) 

    is_staff = models.BooleanField(default=True) 
    is_superuser = models.BooleanField(default=True)   # <=======================> command  when you go for live<=-=-=-=-=-=-=--=-=-=-=->

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_no']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
