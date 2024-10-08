from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserProfileSerializer, GetUserProfileSerializer, GetCommitteeSerializer
from .models import UserProfile, Committee
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def post_userprofile(request):
    try:
        user_id = request.user.id
        user_profile_instance, created = UserProfile.objects.get_or_create(id=user_id)
        
        serializer = UserProfileSerializer(instance=user_profile_instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            
            # Handle committee data
            post_data = request.data
            if post_data.get('committees_count'):
                count = int(post_data.get('committees_count'))
                for index in range(count):
                    key = post_data.get(f'committees_{index}')
                    try:
                        # Assuming 'Committee' is the model you are working with
                        committee_obj = get_object_or_404(Committee, id=key)
                        instance.committee.add(committee_obj)
                    except Committee.DoesNotExist:
                        # Handle the case where the committee with the given ID does not exist
                        print(f"Committee with ID {key} does not exist.")
                    except ValueError:
                        # Handle the case where 'key' is not a valid integer ID
                        print(f"Invalid ID format for committees_{index}")
            
            return Response({'message': 'User Info saved successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Log the actual error for debugging
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def get_userprofile(request):
    if request.method == 'GET':
        try:
            user_id = request.user.id
            user_info_instance = UserProfile.objects.get(id=user_id)
            serializer = GetUserProfileSerializer(user_info_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User Info not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def get_committee(request):
    if request.method == 'GET':
        try:
            commi = Committee.objects.all()
            serializer = GetCommitteeSerializer(commi, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Committee.DoesNotExist:
            return Response({'message': 'Committee not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)