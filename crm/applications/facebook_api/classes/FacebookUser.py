#!/usr/bin/env python

import requests
from applications.facebook_api.tools import FacebookPage

class FacebookUser:
    def __init__(self, user_id, access_token):
        self.user_id = str(user_id)
        self.access_token = str(access_token)

    def get_owned_pages(self):
        
        accounts = requests.get(f'https://graph.facebook.com/{self.user_id}/accounts?access_token={self.access_token}').json()
        
        for account in accounts['data']:
            page = FacebookPage(account['id'], account['accessToken'])