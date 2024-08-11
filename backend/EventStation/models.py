from django.db import models
from UserprofileStation.models import UserProfile,Committee
from VenueStation.models import Venue
import uuid

class EventDetails(models.Model):
    name        = models.CharField(max_length=20,default='')
    description = models.TextField(default='', null=True, blank=True)
    start_date  = models.DateField(auto_now=False, auto_now_add=False)
    end_date    = models.DateField(auto_now=False, auto_now_add=False, null=True)
    location    = models.CharField(max_length=30,default='')
    domain      = models.CharField(max_length=100, blank=True, null=True)
    venue       = models.ForeignKey(Venue, on_delete=models.CASCADE, default='')
    associate   = models.ManyToManyField(UserProfile, blank=True)
    committee   = models.ManyToManyField(Committee, blank=True)
    prize       = models.CharField(default='', max_length=255, blank=True, null=True)
    reg_fee     = models.IntegerField(default=0, null=True, blank=True)
    duration    = models.CharField(max_length=200, null=True, blank=True)
    # approvals   = models.OneToManyField(App
    approve     = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    approved_by_mentor = models.BooleanField(default=False)
    approved_by_hod = models.BooleanField(default=False)
    approved_by_dean = models.BooleanField(default=False)
    unique_id   = models.UUIDField(default=uuid.uuid4, editable=False)
    image       = models.ImageField(upload_to='event/', null=True, blank=True)
    banner      = models.ImageField(upload_to='event/banner/', null=True, blank=True)

    class Meta:
        db_table ='eventStation_eventDetails'

class CastImage(models.Model):
    events = models.ForeignKey(EventDetails, related_name='cast_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/cast', blank=True)

    class Meta:
        db_table ='eventstation_castimages'

class Registration(models.Model):
    event = models.ForeignKey(EventDetails, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')
        db_table = 'eventstation_registration'

choice = (
        ("PENDING", "Pending"),
        ("APPROVE", "Approve"),
        ("DISAPPROVE", "Disapprove"),
)
class Approvals(models.Model):
    event       = models.ForeignKey(EventDetails, on_delete=models.CASCADE)
    user        = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True)
    status      = models.CharField(max_length=10, choices=choice, default='PENDING')
    message     = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Event_Approvals'
    
    def __str__(self):
        return f"{self.event.name}-{self.user.username}-{self.status}-{self.approved_at.strftime('%Y-%m-%d %H:%M:%S')}"