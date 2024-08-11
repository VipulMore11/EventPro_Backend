from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,LoginSerializer, StaffUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from UserprofileStation.models import UserProfile, Role
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import requests

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def signup_view(request):
    if request.method == 'POST':
        reg_serializer = UserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save() 
            refresh = RefreshToken.for_user(new_user)
            role = Role.objects.get(role='BaseUser')
            new_user.role = role
            new_user.save()
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': new_user.role.role
            }, status=status.HTTP_200_OK)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def staff_signup_view(request):
    if request.method == 'POST':
        reg_serializer = StaffUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save() 
            refresh = RefreshToken.for_user(new_user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': ''
            }, status=status.HTTP_200_OK)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        mutable_data = request.data.copy()
        
        try:
            user =UserProfile.objects.get(email=mutable_data.get('email'))
        except UserProfile.DoesNotExist:
            return Response({'error': 'No account found with this email.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LoginSerializer(data=mutable_data, context={'request': request})
        try:
            if serializer.is_valid():
                userprofile= UserProfile.objects.get(email=user)
                role = getattr(userprofile.role, 'role', None)
                refresh = RefreshToken.for_user(user)
                response = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': role
                }
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def google_signup_view(request):
    google_token = request.data.get('access_token')
    if not google_token:
        return Response({'error': 'Access token required'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify the token with Google
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': google_token}
    user_info_response = requests.get(user_info_url, params=params)

    if user_info_response.status_code != 200:
        return Response({'error': 'Invalid Google token'}, status=status.HTTP_400_BAD_REQUEST)

    user_info = user_info_response.json()
    email = user_info.get('email')

    # Get or create the user
    user, created = UserProfile.objects.get_or_create(email=email, defaults={'username': email})

    if created:
        # Additional actions if user was created (e.g., create user profile)
        UserProfile.objects.create(user=user, role=Role.objects.get(name='BaseUser'))

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    return Response({
        'refresh': str(refresh),
        'access': str(access),
        'role': 'BaseUser' if created else user.userprofile.role.name,
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def google_login_view(request):
    google_token = request.data.get('access_token')
    if not google_token:
        return Response({'error': 'Access token required'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify the token with Google
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': google_token}
    user_info_response = requests.get(user_info_url, params=params)

    if user_info_response.status_code != 200:
        return Response({'error': 'Invalid Google token'}, status=status.HTTP_400_BAD_REQUEST)

    user_info = user_info_response.json()
    email = user_info.get('email')

    # Get or create the user
    user, created = UserProfile.objects.get_or_create(email=email, defaults={'username': email})

    if created:
        # Additional actions if user was created (e.g., create user profile)
        UserProfile.objects.create(user=user, role=Role.objects.get(name='BaseUser'))

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    return Response({
        'refresh': str(refresh),
        'access': str(access),
        'role': 'BaseUser' if created else user.userprofile.role.name,
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logged out successfully'})
    except Exception as e:
        return Response(status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def seller_signup_view(request):
    if request.method == 'POST':
        reg_serializer = UserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            refresh = RefreshToken.for_user(new_user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
@authentication_classes([SessionAuthentication])
def seller_login_view(request):
    if request.method == 'POST':
        mutable_data             = request.data.copy()
        user                     = UserProfile.objects.get(email=mutable_data.get('email'))
        mutable_data['username'] = user.username
        serializer               = LoginSerializer(data=mutable_data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            response = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
@authentication_classes([])
def forgot_password(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            user = UserProfile.objects.get(email=user_email)
        except UserProfile.DoesNotExist:
            response = {
                'message': 'User with this email does not exist.',
                'success': False 
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # token = UserInfo.objects.get(user=user).token
        token = ''
        reset_url = f'https://localhost:3000/resetpassword/{token}'
        
        subject = 'Password Reset'
        html_content = render_to_string('myform(1).html', {'reset_url': reset_url})
        text_content = strip_tags(html_content)  # Strip HTML tags for plain text version
        
        email = EmailMultiAlternatives(
            subject,
            text_content,  # Plain text content
            settings.EMAIL_HOST_USER,
            [user_email],
        )
        email.attach_alternative(html_content, "text/html")  # Attach HTML content with content type
        
        try:
            email.send()
            response = {
                'message': 'Email sent successfully',
                'success': True
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'message': f'Failed to send email: {str(e)}',
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# @api_view(['POST'])
# @csrf_exempt
# @permission_classes([AllowAny])
# @authentication_classes([])
# def password_save(request):
#     if request.method == 'POST':
#         token = request.POST.get('token').replace("-", "")
#         try:
#             userinfo = UserInfo.objects.get(token=token)
#             user = userinfo.user
#             user_email = user.email
#         except UserInfo.DoesNotExist:
#             response = {
#                 'message': 'Invalid token provided.',
#                 'success': False
#             }
#             return JsonResponse(response, status=400)

#         password = request.POST.get('password')
#         user.set_password(password)
#         user.save()

#         # Send email confirmation
#         subject = 'Password Reset Confirmation'
#         message = 'Your password has been successfully reset.'
#         email = EmailMessage(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [user_email]
#         )

#         try:
#             email.send()
#             response = {
#                 'message': 'Password updated successfully. Confirmation email sent.',
#                 'success': True
#             }
#             return JsonResponse(response, status=200)
#         except Exception as e:
#             response = {
#                 'message': f'Failed to send email confirmation: {str(e)}',
#                 'success': False
#             }
#             return JsonResponse(response, status=500)

