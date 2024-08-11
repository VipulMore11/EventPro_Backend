from django.db import models
import uuid
from django.contrib.auth.models import User
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser,  Group, Permission


class Committee(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(default=None, blank=True, null=True)

    class Meta:
        db_table = 'UserProfileStation_committee'

class Role(models.Model):
    role = models.CharField(max_length=100, default='', blank=True, null=True)

    class Meta: 
        db_table = 'UserProfileStation_role'

    def __str__(self):
        return f"{self.role}"


class UserProfile(AbstractUser):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.BigIntegerField(default=None, null=True, blank=True)
    profile_image = models.ImageField(upload_to='ProfileImages/', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    committee = models.ManyToManyField(Committee, blank=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='userprofile_user_set',  # Custom related_name to avoid conflict
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='userprofile_user_set',  # Custom related_name to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'UserProfile'