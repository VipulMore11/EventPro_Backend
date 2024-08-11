from django.db import models
from UserprofileStation.models import Role, UserProfile

class Admin(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    class Meta:
        db_table ='AdminStation_admin'