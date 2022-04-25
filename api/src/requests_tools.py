#!/usr/bin/env python

from unidecode import unidecode

def application_json():
    return { "content-type" : "application/json" }


def generate_message_payload(recv_id, message_content):
    '''
    Función que genera payload para mensajes privados
    '''
    send_message_data = {
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": recv_id,
        },
        "message": {
            "text": f"Tu mensaje fue: { unidecode(message_content) }. Vamos a contestar tan pronto como podamos!"
        }
    }

    return str(send_message_data)


def generate_reply_button_payload(comment_id, message_content):
    data = {
        "recipient": {
            # "post_id": "101213069228786_106005088749584"
            # Post id es cuando respodemos a un post de un cliente

            "comment_id": str(comment_id)
        },
        
        "message": {
            "attachment":{
                "type":"template",

                # El payload podría ser recibido por parámetro
                "payload": message_content
            }
        }
    }

    return str(data)


def generate_private_reply_payload(comment_id, message_content):
    data = {
        "recipient": {
            "comment_id": str(comment_id)
        },
        
        "message": {
                "text": str(message_content)
        }
    }

    return str(data)
    