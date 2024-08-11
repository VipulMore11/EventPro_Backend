from rest_framework import serializers
from .models import EventDetails, CastImage
from UserprofileStation.serializers import Base64ImageField

class CastImageSerializers(serializers.ModelSerializer):

    class Meta:
        model = CastImage
        fields = ['id', 'cast_images']

class EventSerializers(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    
    class Meta:
        model = EventDetails
        fields = '__all__'