from django.db import models
# from EventStation.models import EventDetails
class Venue(models.Model):
    # event = models.ForeignKey(EventDetails, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    capacity = models.IntegerField(default=0, null=True, blank=True)
    is_available = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        db_table = 'VenueStation_venue'