import json
import random

def get_message_response():
    # Leer mensajes
    with open('messages.json', 'r') as f:
        messages = json.load(f)
    
    # Devolver un mensaje de la lista data
    data = messages.get('data')
    return data[random.randint(0, len(data) - 1)]