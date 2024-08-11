from django.db import models
import uuid
from django.contrib.auth.models import User


class Committee(models.Model):
    name            = models.CharField(max_length=100)
    description     = models.TextField(default=None, blank=True, null=True)

    class Meta:
        db_table = 'UserProfileStation_committee'

class Role(models.Model):
    role            = models.CharField(max_length=100, default='', blank=True, null=True)

    class Meta:
        db_table = 'UserProfileStation_role'


class UserProfile(models.Model):
    unique_id       = models.UUIDField(default=uuid.uuid4, editable=False)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name      = models.CharField(max_length=100, null=True, blank=True)
    last_name       = models.CharField(max_length=100, null=True, blank=True)
    email           = models.EmailField()
    phone_number    = models.BigIntegerField(default=None, null=True, blank=True)
    profile_image   = models.ImageField(upload_to='ProfileImages/', null=True, blank=True)
    role            = models.ForeignKey(Role, on_delete=models.CASCADE)
    committee       = models.ManyToManyField(Committee, blank=True) 
    branch          = models.CharField(max_length=100, blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'UserProfileStation_userprofile'

