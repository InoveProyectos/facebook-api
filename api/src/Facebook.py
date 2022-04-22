#!/usr/bin/env python

'''
Este módulo se va a encargar de interactuar con la GRAPH API
Para poder usarlo, es necesario que estén declarado ACCESS_TOKEN y PAGE_ID
como variable de entorno
'''

import requests
from dotenv import load_dotenv
import os, sys, inspect

# Setear import path en directorio api
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src import requests_tools

from tools.pretty_print import pretty_print_json

# facebook sdk
import facebook as sdk

load_dotenv()

access_token = os.getenv('ACCESS_TOKEN')
graph_api = sdk.GraphAPI(access_token)


class Facebook:
    def __init__(self):
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.page_id = os.getenv('PAGE_ID')
        self.send_message_url = "https://graph.facebook.com/v13.0/me/messages?access_token=" + str(access_token)

    def send_message(self, recv_id, message_content):
        '''
        Función que recibe id del receptor del mensaje (recv_id) y contenido
        del mensaje (message_content) y envía el mensaje por privado al usuario.
        Esta función es usada para responder mensajes de messenger, no para responder por privado
        a comentarios de nuestras publicaciones
        '''
        payload = requests_tools.message_data(recv_id, message_content)
        header = requests_tools.application_json()

        requests.post(url = self.send_message_url, 
                    headers = header, 
                    data = payload)
    

    def get_page_posts(self):
        '''
        Función que retorna todos los Post propios de una página
        '''
        url = f"https://graph.facebook.com/v13.0/me/posts?id={ str(self.page_id) }&access_token={ str(self.access_token) }"

        response = requests.get(url = url)
        
        return response.json()

    
    def get_post_comments(self, post_id):
        '''
        Obtener los comentarios de un post
        '''
        url = f"https://graph.facebook.com/v13.0/{ str(post_id) }/comments?access_token={ str(self.access_token) }"

        response = requests.get(url = url)

        return response.json()


    def private_reply_buttons(self, comment_id, message_content : dict):
        '''
        Enviar a un usuario que comentó una publicación, un mensaje por privado, la gracia
        del template, es que le da al usuario una serie de botones, para que pueda seleccionar uno de ellos.

        El parámetro message_content debe ser del siguiente estilo
        {
            "template_type":"button",
            "text":"Que curso te interesa mas?:",
            "buttons":[
                {
                    "type": "postback",
                    "title": "Python Django",
                    "payload": "PD"
                },
                {
                    "type": "postback",
                    "title": "DW Javascript",
                    "payload": "JS"
                },
                {
                    "type": "postback",
                    "title": "Python Inicial",
                    "payload": "PI"
                }
            ]
        }
        '''
        url = self.send_message_url

        header = requests_tools.application_json()
        payload = requests_tools.generate_payload_reply_button(comment_id, message_content)

        requests.post(url = url, headers = header, data = payload)


    def private_reply(self, comment_id, message_content):
        '''
        Responder con un mensaje a alguien que haya comentado un post
        '''

        url = self.send_message_url

        header = requests_tools.application_json()
        payload = requests_tools.generate_payload_reply(comment_id, message_content)

        requests.post(url = url, headers = header, data = payload)


    def make_post(self, message):
        '''
        Uso Facebook SDK para realizar un post que contiene un mensaje
        '''
        graph_api.put_object("me", "feed", message = message)


    def make_post_image(self, image_path, message):
        '''
        Uso Facebook SDK para realizar un post que contiene una imagen y un mensaje 
        '''
        graph_api.put_photo(open(image_path, "rb"), message = message)


    def comment(self, post_id, message):
        '''
        Este método se encarga de publicar un comentario, el post_id puede ser el id de un post
        o el id de otro comentario, y la página hará una respuesta al comentario
        '''
        graph_api.put_object(str(post_id), "comments", message = message)
