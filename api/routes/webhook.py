#!/usr/bin/env python

from flask import Blueprint, Response, request
from dotenv import load_dotenv
import os, sys, inspect

# Setear import path en directorio api
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from tools.colors import *

from src.Facebook import *

# Creo un objeto facebook para luego interactuar con la página
fb = Facebook()

# Cargar variables de entorno (archivo .env)
load_dotenv()

# Blueprint que va a contener todos los endpoints del messenger webhook
webhook = Blueprint('webhook', __name__)

# Agregar soporte de peticiones de tipo GET al webhook
@webhook.route('/webhook', methods = ['GET'])
def webhook_get():
    # Código de verificacion, string arbitrario
    verify_token = os.getenv('VERIFY_TOKEN')

    # Parsear parametros recibidos por url
    mode = str(request.args.get('hub.mode'))
    token = str(request.args.get('hub.verify_token'))
    challenge = str(request.args.get('hub.challenge'))

    # Verificar si token y mode fueron enviados en la petición
    if mode and token:

        # Verificar que mode y token coincidan con los valores esperados
        if mode == 'subscribe' and token == verify_token:

            # Enviar en la respuesta el token challenge que envió que llegó en request
            print(f'{OKGREEN} WEBHOOK_VERIFIED')
            return Response(challenge, status = 200)
        
    # 'Forbidden', ocurre cuando el token no coincide
    print(f'{FAIL} Tokens does not match')
    return Response(status = 403)


@webhook.route('/webhook', methods = ['POST'])
def webhook_post():
    # Obtener body del request
    body = request.get_json()
    print(body) 

    if body.get('object') == 'page':
        webhook_event = body.get('entry')[0].get('messaging')[0].get('message')
        print('Webhook event: ' + OKGREEN + str(webhook_event))

        ###### PROVISORIO: Enviar una respuesta al mensaje ######

        recv_id = str(body.get('entry')[0].get('messaging')[0].get('sender').get('id'))
        message_content = webhook_event.get('text')
        fb.send_message(recv_id, message_content)

        ###### FIN DE RESPUESTA GENERADA #######

        # Return '200 OK' response to all requests
        return Response('EVENT_RECEIVED', status = 200)

    # Returns a '404 Not Found' if event is not from a page subscription
    print(f'{FAIL} 404 Not Found: {body}')
    return Response(status = 404)
