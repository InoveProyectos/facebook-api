#!/usr/bin/env python

'''
Este archivo tiene el objetivo de cumplir la siguiente rutina
1. Obtener todas las publicaciones
2. Obtener todos los comentarios
3. Responder a todos los comentarios de forma pública
4. Responder a todos los comentarios de forma privada
'''

from Facebook import Facebook

import json
from datetime import datetime
from pytz import timezone

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
    feed = get_feed(access_token, page_id, timezone)

    for post in feed.get('data'):
        for comment in post.get('comments'):
            if not already_liked_by(page_id, comment):
                fb.put_like(comment.get('id'))

                # TODO: Generar una respuesta que tenga sentido
                response = 'Respuesta por defecto :)'

                fb.comment(comment.get('id'), 'Te enviamos información por privado! :)')
                fb.private_reply(comment.get('id'), response)

                # TODO: Almacenar datos del usuario

    print(json.dumps(feed, indent = 4))


def get_feed(access_token, page_id, timezone = 'America/Argentina/Buenos_Aires'):
    '''
    Función que se encarga de agregar valores interesantes para el usuario, entre
    esos valores se encuentran
    - los posts
    - los comentarios de cada post
    - los likes de cada comentario
    - los likes de cada post
    '''

    fb = Facebook(access_token, page_id)

    # Obtener el feed de una página con su zona horaria
    feed = set_user_timezone(fb.get_page_posts(), timezone)

    for post in feed.get('data'):

        # Ir a buscar los comentarios del post, con sus respectivos likes
        comments = fb.get_post_comments(post.get('id')).get('data')
        
        for comment in comments:
            comment_likes = fb.get_post_likes(comment.get('id'))
            comment['likes_amount'] = comment_likes.get('likes').get('summary').get('total_count')
            comment['users_that_liked'] = comment_likes.get('likes').get('data')

        # Agregar la key comments en el post
        post['comments'] = comments
        
        # Agregar información acerca de los likes del post
        likes = fb.get_post_likes(post.get('id'))
        post['likes_amount'] = likes.get('likes').get('summary').get('total_count')
        post['users_that_liked'] = likes.get('likes').get('data')
    
    return feed


def set_user_timezone(response_dict, user_timezone):
    '''
    Este método se encarga de devolver el mismo response_dict que recibe, pero modificando cada instancia
    de created_time con la zona horaria del usuario
    '''
    for value in response_dict.get('data'):
        # obtener created time
        created_time = value.get('created_time')

        # modificar el string para que tenga formato 'iso'
        created_time = created_time[:-2] + ':' + created_time[-2:]

        created_time = datetime.fromisoformat(created_time).astimezone(timezone(user_timezone))

        value['created_time'] = str(created_time)        

    return response_dict


def already_liked_by(id, comment):
    '''
    Devuelve true si alguno de los usuarios que dieron like coincide con el que nosotros buscamos
    '''
    return any([True if user.get('id') == id else False for user in comment.get('users_that_liked')])
    