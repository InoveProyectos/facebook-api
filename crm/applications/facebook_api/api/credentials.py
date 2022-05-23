#!/usr/bin/env python

from applications.facebook_api.api.serializers import CredentialSerializer

from applications.facebook_api.models import Credential

# REST Framework api tools
from rest_framework.generics import (
    ListAPIView,  # (GET) Listar todos los elementos en la entidad  
    CreateAPIView,  # (POST) Inserta elementos 
    ListCreateAPIView,  # (GET-POST) Para leer e insertar elementos 
    RetrieveUpdateAPIView,  # (PUT) Recuperar y actualizar elementos
    DestroyAPIView  # (DELETE) Eliminar elementos de la base de datos
)

from rest_framework.permissions import IsAuthenticated, IsAdminUser


def generic_header_message(method : str):
    '''
    Funcion auxiliar para documentar el header de cada endpoint
    '''
    
    header = f'''
        headers = {{
            'Authorization': 'Token <your-token>',
            'actions': {method.upper()},
            'Content-Type': 'application/json',
            'Cookie': 'csrftoken=<your-csrftoken>'
        }}'''

    return header


class GetCredentialAPIView(ListAPIView):
    __doc__ = f'''
    `[GET METHOD]`
    Obtener todos los elementos de la entidad Credentials
    
    {generic_header_message('GET')}
    '''

    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class PostCredentialAPIView(CreateAPIView):
    __doc__ = f'''
    `[POST METHOD]
    Insertar credenciales de un usuario en la base de datos
    
    {generic_header_message('POST')}
    '''

    queryset = Credential.objects().all()
    serializer_class = CredentialSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

  
class ListCreateCredentialAPIView(ListCreateAPIView):
    __doc__ = f'''
    `[GET-POST METHOD]
    Obtener todos los elementos de la entidad Credential o insertar una lista dentro de la entidad Credential
    
    {generic_header_message('GET-POST')}
    '''

    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class RetrieveUpdateCredentialAPIView(RetrieveUpdateAPIView):
    __doc__ = f'''
    `[GET-PUT-PATCH METHOD]
    Actualizar un elemento de la entidad Credential o simplemente obtener dicho elemento usando su primary key
    
    {generic_header_message('GET-PUT-PATCH')}
    '''

    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DestroyCredentialAPIView(DestroyAPIView):
    __doc__ = f'''
    `[DELETE METHOD]
    Eliminar un elemento de la entidad Credential con usando su primary key
    
    {generic_header_message('GET-PUT-PATCH')}
    '''

    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
