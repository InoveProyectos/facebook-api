#!/usr/bin/env python

from django.db import models

from django.contrib.auth.models import User

import django

class Credential(models.Model):
    '''
    Tabla que contiene las credenciales de un usuario de Facebook
    '''
    id = models.AutoField(db_column='Credential ID', primary_key=True)

    user = models.ForeignKey(User, verbose_name="User",
                             on_delete=models.DO_NOTHING, default=1, blank=True)

    facebook_id = models.CharField(db_column='Facebook ID', max_length=500, blank = True)
    
    access_token = models.CharField(db_column='Access Token', max_length=500, blank = True)
    
    class Meta:
        db_table = 'facebook_api_credentials'
        verbose_name = 'Credential'
        verbose_name_plural = 'Credentials'

    def __str__(self):
        return f'{self.user.username} - {self.access_token}'
