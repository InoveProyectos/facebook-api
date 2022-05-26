#!/usr/bin/env python

from rest_framework import serializers

from applications.facebook_api.models import Credential
from django.contrib.auth.models import User

class CredentialSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(write_only=True,
                                                   queryset=User.objects.all()) 

    class Meta:
        model = Credential
        fields = ('id', 'user', 'access_token', 'expires_in', 'created_at', 'updated_at')
