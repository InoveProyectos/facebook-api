#!/usr/bin/env python

import requests
from applications.facebook_api.classes.FacebookPage import FacebookPage

class FacebookUser:
    def __init__(self, user_id, access_token):
        self.user_id = str(user_id)
        self.access_token = str(access_token)


    def get_owned_pages(self):
        '''
        Obtener todas las páginas que administra el usuario
        
        @return: lista de objetos de tipo FacebookPage, con las imagenes (atributo picture) ya seteadas
        '''
        accounts = requests.get(f'https://graph.facebook.com/{self.user_id}/accounts?access_token={self.access_token}').json()
        
        pages = [FacebookPage(account['id'], account['access_token'], account['name']) for account in accounts['data']]
        
        # Set all profile pictures
        [(lambda x: x.set_picture())(x) for x in pages]

        return pages


    def is_admin(self, page_id):
        '''
        Devuelve True si el usuario tiene permisos para administrar una página por su ID
        '''
        pages = self.get_owned_pages()

        return str(page_id) in [(lambda x: x.id)(x) for x in pages]
