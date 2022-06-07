#!/usr/bin/env python

from tabnanny import verbose
from django.db import models

from django.contrib.auth.models import User

class Credential(models.Model):
    '''
    Tabla que contiene las credenciales de un usuario de Facebook
    '''
    id = models.AutoField(db_column='Credential ID', primary_key=True)

    user = models.ForeignKey(User, verbose_name="User",
                             on_delete=models.DO_NOTHING, default=1, blank=True)

    facebook_id = models.CharField(db_column='User Facebook ID', max_length=500, blank = True)
    
    access_token = models.CharField(db_column='Access Token', max_length=500, blank = True)
    
    class Meta:
        db_table = 'facebook_api_credentials'
        verbose_name = 'Credential'
        verbose_name_plural = 'Credentials'

    def __str__(self):
        return f'{self.user.username} - {self.access_token}'


class Page(models.Model):
    '''
    Tabla que contiene páginas de facebook
    '''
    id = models.AutoField(verbose_name = 'ID', primary_key=True)

    page_id = models.BigIntegerField(verbose_name = 'Facebook Page ID')

    access_token = models.CharField(verbose_name = 'Facebook Access Token', max_length=500, blank = True)

    owner = models.ForeignKey(Credential, verbose_name="Credential", on_delete=models.DO_NOTHING)

    name = models.CharField(verbose_name = 'Facebook Page Name', max_length=255, blank = True)

    url = models.CharField(verbose_name = 'Facebook Page Link', max_length=255, blank = True)

    picture = models.CharField(verbose_name = 'Facebook Page Picture', max_length=500, blank = True)

    posts_respondidos = models.IntegerField(verbose_name = 'Posts Respondidos', default=0)

    mensajes_respondidos = models.IntegerField(verbose_name = 'Mensajes Respondidos', default=0)


class Response(models.Model):
    '''
    Tabla que contiene respuestas de mensajes de facebook registradas por cada página
    '''
    id = models.AutoField(verbose_name = 'ID', primary_key=True)

    page = models.ForeignKey(Page, verbose_name = "Page", on_delete=models.DO_NOTHING)

    tag = models.CharField(verbose_name = 'Tag', max_length=50, blank = True)  

    message = models.CharField(verbose_name = 'Message', max_length=500, blank = True)


class Message(models.Model):
    '''
    Tabla que contiene mensajes de facebook registrados por cada página
    '''
    id = models.AutoField(verbose_name = 'ID', primary_key=True)

    page = models.ForeignKey(Page, verbose_name = "Page", on_delete = models.DO_NOTHING)

    sender_id = models.CharField(verbose_name = 'User Facebook ID', max_length=500)

    sender_name = models.CharField(verbose_name = 'User Facebook Name', max_length=255, blank = True)

    sender_picture = models.CharField(verbose_name = 'User Facebook Picture', max_length=500, blank = True)

    content = models.CharField(verbose_name = 'Message', max_length=500)
