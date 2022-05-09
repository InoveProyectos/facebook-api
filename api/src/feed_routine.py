#!/usr/bin/env python

'''
Este archivo tiene el objetivo de cumplir la siguiente rutina
1. Obtener todas las publicaciones
2. Obtener todos los comentarios
3. Responder a todos los comentarios de forma pública
4. Responder a todos los comentarios de forma privada
'''

from Facebook import Facebook

def answer_all_feed_comments(access_token, page_id, timezone = 'America/Argentina/Buenos_Aires'):
    '''
    @param page_id: id de la página de la aplicación
    @access_token: token de acceso de la aplicación a la página, se obtiene
                   en el apartado messenger webhooks del dashboard
    @timezone: objeto de tipo timezone con la zona horaria del usuario, acá están todas las
               disponibles https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
    '''
    fb = Facebook(access_token  = access_token, page_id = page_id)

    # Obtener todos los posts con el timezone del cliente
    feed = fb.get_feed(timezone)

    for post in feed.get('data'):
        for comment in post.get('comments'):
            if not fb.already_liked(page_id, comment):
                fb.put_like(comment.get('id'))

                # TODO: Generar una respuesta que tenga sentido
                response = 'Respuesta por defecto :)'

                fb.comment(comment.get('id'), 'Te enviamos información por privado! :)')
                fb.private_reply(comment.get('id'), response)

                # TODO: Almacenar datos del usuario
    
