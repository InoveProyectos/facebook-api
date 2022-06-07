#!/usr/bin/env python

from applications.facebook_api.models import Credential

import requests

def get_user_credentials(user):
    '''
    Obtener las credenciales de un usuario

    @param user: Objeto User que contiene id para buscar credenciales
    
    @return: Objeto Credential con las credenciales del usuario
    '''

    try:
        return Credential.objects.get(user=user.id)
    
    except Credential.DoesNotExist:
        return None


def token_is_valid(page_token, user_token):
    '''
    Verifica si el token de usuario sigue siendo valido
    '''
    url = 'https://graph.facebook.com/debug_token'
    params = {
        'input_token': page_token,
        'access_token': user_token
    }

    response = requests.get(url, params=params)

    return (response.json()['data']['is_valid'])
    