from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import VenueSerializer
from .models import Venue

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_venue(request):
    if request.method == 'POST':
        try:
            user_id = request.user.id
            mutable_data = request.data.copy()
            mutable_data['seller'] = user_id
            serializer = VenueSerializer(data=mutable_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
@permission_classes([AllowAny])
def get_venue(request):
    if request.method == 'GET':
        venue_id = request.GET.get('venue_id')
        try:
            if venue_id:
                product = Venue.objects.get(id=venue_id)
                serializer = VenueSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                products = Venue.objects.all().order_by('-id')
                serializer = VenueSerializer(products, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Venue.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

