#!/usr/bin/env python

from django.http import HttpResponse
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User
from applications.facebook_api.models import Credential

from datetime import datetime, timedelta
import requests

import pytz
import sys, os

utc=pytz.UTC

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_user_credentials(request):
    data = request._data
    fb_id = data.get('userId')
    access_token = data.get('accessToken')
    username = data.get('username')

    if not(fb_id and access_token and username):   
        print('No se recibieron todos los datos necesarios')    
        print(fb_id, access_token, username)
        return HttpResponse(status = 400, content = 'Bad request')

    try:

        user_obj = User.objects.get(username = username)
        
        credential_obj = Credential.objects.filter(user = user_obj.id).first()  

        if not credential_obj:

            long_lived_token = get_long_lived_token(str(os.getenv('APP_ID')), str(os.getenv('APP_SECRET')), access_token)

            credential_obj = Credential.objects.create(
                user=user_obj, facebook_id = fb_id, access_token=long_lived_token)
            
            credential_obj.save()

        else:
            long_lived_token = get_long_lived_token(os.getenv('APP_ID'), os.getenv('APP_SECRET'), access_token)
            credential_obj.access_token = long_lived_token
            credential_obj.save()

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return HttpResponse(status = 400, content = f'Bad request: {e}')
    
    return HttpResponse(status = 200, content = 'OK')


def get_long_lived_token(user_access_token):
    '''
    Genera un access token de larga duración (50 días)
    '''
    url = 'https://graph.facebook.com/oauth/access_token'
    
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': str(os.getenv('app_id')),
        'client_secret': str(os.getenv('app_secret')),
        'fb_exchange_token': user_access_token
    }

    response = requests.get(url, params=params)
    return response.json()['access_token']
