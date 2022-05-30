#!/usr/bin/env python

import requests

class FacebookPage:
    def __init__(self, id, access_token):
        self.id = str(id)
        self.access_token = str(access_token)
    
    
    def get_picture(self):
        '''
        Obtener la imagen de perfil de la página

        @return string con la url de la imagen
        '''
        data = requests.get(f'https://graph.facebook.com/v14.0/{self.id}/picture?redirect=0&access_token={self.access_token}').json()

        return data['data']['url']
    