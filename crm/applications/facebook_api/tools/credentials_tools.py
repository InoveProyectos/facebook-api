#!/usr/bin/env python

from applications.facebook_api.models import Credential
from django.contrib.auth.models import User

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
