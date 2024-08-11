from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import serializers    
from django.contrib.auth import authenticate
from UserprofileStation.models import UserProfile, Role

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email','password', 'username', 'first_name', 'last_name']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        if not email:
            raise ValueError(_('The Email must be set'))
        user = UserProfile(email=email, username=username)
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active= True
        user.save()
        return user

class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email','password', 'username', 'first_name', 'last_name']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        if not email:
            raise ValueError(_('The Email must be set'))
        user = UserProfile(email=email, username=username)
        user.set_password(password)
        user.role = None
        user.first_name = first_name
        user.last_name = last_name
        user.is_active= True
        user.save()
        return user

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = UserProfile.objects.get(email=data.get('email'))
        password = data.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if user is not None:
                if user.is_active:
                    return user
                else:
                    raise AuthenticationFailed(detail="User account is not active.", code="account_disabled")
            else:
                raise AuthenticationFailed(detail="Invalid credentials. Please try again.", code="invalid_credentials")
        raise AuthenticationFailed(detail="Both email and password are required.", code="missing_fields")
