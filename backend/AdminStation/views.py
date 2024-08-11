from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from UserprofileStation.serializers import UserProfileSerializer
from UserprofileStation.models import UserProfile


@api_view(['POST'])
@permission_classes([IsAdminUser])
@authentication_classes([])
def add_role(request):
    try:
        user_id = request.data.get('user_id')
        new_role = request.data.get('new_role')

        user_profile = UserProfile.objects.get(user_id=user_id)
        user_profile.role = new_role
        user_profile.save()

        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': f'Failed to update user role: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)