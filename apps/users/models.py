from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone


class UserManager(BaseUserManager):
   def _create_user(self, username, email, password, **extra_fields):
      if not username:
         raise ValueError("The given username must be set")
      email = self.normalize_email(email)
      GlobalUserModel = apps.get_model(
         self.model._meta.app_label, self.model._meta.object_name
      )
      username = GlobalUserModel.normalize_username(username)
      user = self.model(username=username, email=email, **extra_fields)
      user.password = make_password(password)
      user.save(using=self._db)
      return user

   def create_user(self, username, email=None, password=None, **extra_fields):
      extra_fields.setdefault("is_staff", False)
      extra_fields.setdefault("is_superuser", False)
      return self._create_user(username, email, password, **extra_fields)

   def create_superuser(self, username, email=None, password=None, **extra_fields):
      extra_fields.setdefault("is_staff", True)
      extra_fields.setdefault("is_superuser", True)

      if extra_fields.get("is_staff") is not True:
         raise ValueError("Superuser must have is_staff=True.")
      if extra_fields.get("is_superuser") is not True:
         raise ValueError("Superuser must have is_superuser=True.")

      return self._create_user(username, email, password, **extra_fields)

   def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
      if backend is None:
         backends = auth._get_backends(return_tuples=True)
         if len(backends) == 1:
            backend, _ = backends[0]
         else:
            raise ValueError(
               "You have multiple authentication backends configured and "
               "therefore must provide the `backend` argument."
            )
      elif not isinstance(backend, str):
         raise TypeError(
            "backend must be a dotted import path string (got %r)." % backend
         )
      else:
         backend = auth.load_backend(backend)
      if hasattr(backend, "with_perm"):
         return backend.with_perm(
            perm,
            is_active=is_active,
            include_superusers=include_superusers,
            obj=obj,
         )
      return self.none()


class User(AbstractBaseUser, PermissionsMixin):
   username_validator = UnicodeUsernameValidator()
   username = models.CharField(
      _("username"),
      max_length=150,
      unique=True,
      help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
      validators=[username_validator],
      error_messages={"unique": _("A user with that username already exists.")},
   )
   first_name = models.CharField(_("first name"), max_length=150, blank=True)
   last_name = models.CharField(_("last name"), max_length=150, blank=True)
   email = models.EmailField(_("email address"),max_length=256, null=True, blank=True)
   phone_number = models.CharField(_("phone number"),max_length=14, null=True, blank=True)
   is_staff = models.BooleanField(_("staff status"), default=False)
   is_active = models.BooleanField(_("active"), default=True)
   date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
   date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
   objects = UserManager()
   EMAIL_FIELD = "email"
   USERNAME_FIELD = "username"
   REQUIRED_FIELDS = []
   
   class Meta:
      verbose_name = _("user")
      verbose_name_plural = _("users")
      abstract = False
      swappable = "AUTH_USER_MODEL"

   def clean(self):
      super().clean()
      self.email = self.__class__.objects.normalize_email(self.email)

   def email_user(self, subject, message, from_email=None, **kwargs):
      """Send an email to this user."""
      send_mail(subject, message, from_email, [self.email], **kwargs)





# class MyUserManager(BaseUserManager):
#    def create_user(self, email, date_of_birth, password=None):
#       if not email:
#          raise ValueError("Users must have an email address")

#       user = self.model(
#          email=self.normalize_email(email),
#          date_of_birth=date_of_birth,
#       )

#       user.set_password(password)
#       user.save(using=self._db)
#       return user

#    def create_superuser(self, email, date_of_birth, password=None):
#       """
#       Creates and saves a superuser with the given email, date of
#       birth and password.
#       """
#       user = self.create_user(
#          email,
#          password=password,
#          date_of_birth=date_of_birth,
#       )
#       user.is_admin = True
#       user.save(using=self._db)
#       return user


# class MyUser(AbstractBaseUser):
#    email = models.EmailField(verbose_name="email address", max_length=255, unique=True,)
#    date_of_birth = models.DateField()
#    is_active = models.BooleanField(default=True)
#    is_admin = models.BooleanField(default=False)

#    objects = MyUserManager()

#    USERNAME_FIELD = "email"
#    REQUIRED_FIELDS = ["date_of_birth"]

#    def __str__(self):
#       return self.email

#    def has_perm(self, perm, obj=None):
#       "Does the user have a specific permission?"
#       # Simplest possible answer: Yes, always
#       return True

#    def has_module_perms(self, app_label):
#       "Does the user have permissions to view the app `app_label`?"
#       # Simplest possible answer: Yes, always
#       return True

#    @property
#    def is_staff(self):
#       "Is the user a member of staff?"
#       # Simplest possible answer: All admins are staff
#       return self.is_admin

