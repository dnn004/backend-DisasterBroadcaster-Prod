from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from disaster_broadcaster.models.Country import Country
from django.db import models
from django.core.validators import RegexValidator
from disaster_broadcaster.filepaths.FilePath import FilePath

class UserManager(BaseUserManager):
  def create_user(self, password, **kwargs):
    user = User(**kwargs)
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, username, email, password):
    """
    Creates and saves a superuser with the given email and password.
    """
    user = self.create_user(
      username=username,
      password=password,
      email=email,
    )
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user

class User(AbstractBaseUser, PermissionsMixin):
  objects = UserManager()
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  # Contact Information
  email = models.EmailField(unique=True, null=True)

  # Validation Information
  username = models.CharField(default='', max_length=64, unique=True)
  password = models.CharField(max_length=120)
  answer = models.CharField(max_length=120)

  # Public Information
  avatar = models.ImageField(default='default-avatar.jpg', editable=True, upload_to=FilePath.avatar)
  country_id = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)

  # Bookkeeping Information
  date_created = models.DateTimeField(auto_now_add=True, null=True)
  date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

  # Account Status Information
  is_deleted = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  def delete(self, using=None, keep_parents=False):
    """
    Soft deletion of Users
    """
    self.is_deleted = True
    self.save()
  
  def check_password_auth(self, password):
    return self.check_password(password)

  def save(self, *args, **kwargs):
    if self.pk is None:
      saved_avatar = self.avatar
      self.avatar = None
      super(User, self).save(*args, **kwargs)
      self.avatar = saved_avatar
      
    super(User, self).save(*args, **kwargs)