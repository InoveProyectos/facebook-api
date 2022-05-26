#!/usr/bin/env python

from django.http import HttpResponse
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User
from applications.facebook_api.models import Credential

from datetime import datetime
import requests
from crm.settings import get_env


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def credentials_status(request):
    fb_id = request.POST.get('userId')
    access_token = request.POST.get('accessToken')
    username = request.POST.get('username')

    if not(fb_id and access_token and username):
        return HttpResponse(status = 400, content = 'Bad request')

    try:
        user_obj = User.objects.get(username = username)
        credential_obj = Credential.objects.filter(user_id = user_obj).first()

        if not credential_obj:
            # Si el usuario aún no tenía creadas unas credenciales, crear unas
            long_lived_token = get_long_lived_token(get_env('APP_ID'), get_env('APP_SECRET'), access_token)
            credential_obj = Credential.objects.create(
                user=user_obj, access_token=long_lived_token, expires_in=50, created_at=datetime.now())
            
            credential_obj.save()

        elif token_expired(credential_obj.access_token):
            # Si el token ya venció, actualizarlo
            long_lived_token = get_long_lived_token(get_env('APP_ID'), get_env('APP_SECRET'), access_token)
            credential_obj.access_token = long_lived_token
            credential_obj.save()

    except Exception as e:
        return HttpResponse(status = 400, content = f'Bad request: {e}')

    return HttpResponse(status = 200, content = 'OK')


def get_long_lived_token(app_id, app_secret, user_access_token):
    '''
    Genera un access token de larga duración (50 días)
    '''
    url = 'https://graph.facebook.com/oauth/access_token'
    
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': user_access_token
    }

    r = requests.get(url, params=params)
    return r.json()['access_token']


def token_expired(username):
    '''
    Verifica si el token de usuario se venció
    '''
    user_obj = User.objects.get(username = username)
    credential_obj = Credential.objects.filter(user_id = user_obj).first()
    
    if credential_obj:
        # Si aún no se cumplieron los 50 días, retornar True
        if credential_obj.created_at + datetime.timedelta(days=credential_obj.expires_in) >= datetime.now():
            return True
        else:
            return False
    else:
        return False