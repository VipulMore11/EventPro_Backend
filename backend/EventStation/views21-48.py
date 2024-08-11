###############Rest Framework Import###########################################
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
################Response###########################
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
################Email Import###########################
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
################Model Import###########################
from django.contrib.auth.models import User
from .models import EventDetails
from UserprofileStation.models import Committee
from django.db.models import Q,Count, Sum, Max, FloatField
################Serializers Import###########################
from .serializers import EventSerializers

@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
@authentication_classes([])
def event_info(request):
    try:
        slug = request.GET.get('event_unique_id')
        if slug:
            slug = slug.replace("-", "")
            event_obj = get_object_or_404(EventDetails, unique_id=slug)
            event_serializer = EventSerializers(event_obj)
            response_data = {'event': event_serializer.data}
        else:
            event_objs = EventDetails.objects.all()
            event_serializer = EventSerializers(event_objs, many=True)  # Corrected line
            response_data = {'events': event_serializer.data}
        return JsonResponse(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        response_data = {'message': f'Failed to retrieve event information: {str(e)}'}
        return JsonResponse(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
@authentication_classes([])
def event_details(request):
    over_all_search = request.POST.get('searchValue')
    field_mapping = {
        0: 'name__icontains',
        1: 'location__icontains',
    }
    advance_filter = Q()
    if over_all_search:
        overall_search_filter = Q()
        for field in field_mapping.values():
            overall_search_filter |= Q(**{field: over_all_search})
        advance_filter |= overall_search_filter
    try:
        event_obj = EventDetails.objects.filter(advance_filter)
        event_obj = EventSerializers(event_obj,many=True)
        response = {
            'event':event_obj.data
        }
        return JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as e:
        response = {
            'message': f'Failed to send email: {str(e)}',
        }
        return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
@authentication_classes([])
def event_add(request):
    try:
        post_data = request.POST.copy()
        try:
            slug = request.GET.get('event_unique_id').replace("-","")
            print(slug)
            event_obj = EventDetails.objects.get(unique_id=slug)
        except:
            event_obj = None
        event_serailizer = EventSerializers(instance=event_obj,data=request.POST)
        if event_serailizer.is_valid():
            instance = event_serailizer.save()
            print()
            if post_data.get('associate', None):
                count = int(post_data.get('associate'))
                for index in range(count):
                    key = post_data.get(f'associate_{index}')
                    try:
                        user_obj = get_object_or_404(User, id=key)
                        instance.associate.add(user_obj)
                    except user_obj.DoesNotExist:
                        print(f"Client account with ID {key} does not exist.")
                    except ValueError:
                        print(f"Invalid ID format for user_{index}")      

                        
            if post_data.get('committee_count', None):
                count = int(post_data.get('committee_count'))
                for index in range(count):
                    key = post_data.get(f'committee_{index}')
                    try:
                        committee_obj = get_object_or_404(Committee, id=key)
                        instance.committee.add(committee_obj)
                    except committee_obj.DoesNotExist:
                        print(f"Client account with ID {key} does not exist.")
                    except ValueError:
                        print(f"Invalid ID format for committee_{index}")  
            response = {
                'event':event_serailizer.data
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
        else :
            response = {
            'message': f'Failed to save : {str(event_serailizer.errors)}',
        }
        return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        response = {
            'message': f'{str(e)}',
        }
        return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
