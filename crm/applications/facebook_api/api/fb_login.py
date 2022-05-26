from django.http import HttpResponse
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def credentials_status(request):
    fb_id = request.POST.get('userId')
    access_oken = request.POST.get('accessToken')