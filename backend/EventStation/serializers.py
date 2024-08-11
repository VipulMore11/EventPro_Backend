from rest_framework import serializers
from .models import EventDetails, Registration, Approvals
from UserprofileStation.serializers import Base64ImageField

class ApprovalsSerializer(serializers.ModelSerializer):
    class Meta:
        depth=1
        model = Approvals
        fields = '__all__'

class EventSerializers(serializers.ModelSerializer):
    approvals = ApprovalsSerializer(many=True, read_only=True, source='approvals_set')
    image = Base64ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    banner = Base64ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        # depth = 1
        model = EventDetails
        fields = '__all__'

class GetEventSerializers(serializers.ModelSerializer):
    approvals = ApprovalsSerializer(many=True, read_only=True, source='approvals_set')
    image = Base64ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    banner = Base64ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    total_registrations = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        model = EventDetails
        fields = '__all__'

    def get_total_registrations(self, obj):
        return obj.registrations.count()

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

class GetRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Registration
        fields = '__all__'