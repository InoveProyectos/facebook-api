#!/usr/bin/env python

'''
Este módulo se va a encargar de interactuar con la GRAPH API
Para poder usarlo, es necesario que estén declarado ACCESS_TOKEN y PAGE_ID
como variable de entorno
'''

import requests
from datetime import datetime
from pytz import timezone
import os

# facebook sdk
import facebook as sdk
import applications.facebook_api.tools.requests_tools as requests_tools

class Facebook:
    def __init__(self, access_token : str, page_id : str):
        self.access_token = access_token
        self.page_id = page_id
        
        # Usar SDK de Facebook
        self.graph_api = sdk.GraphAPI(access_token)
        self.send_message_url = "https://graph.facebook.com/v13.0/me/messages?access_token=" + str(access_token)


    def get_feed(self, timezone = 'America/Argentina/Buenos_Aires'):
        '''
        Obtener el feed COMPLETO de una página y mostrarlo con la zona horaria solicitada
        esto incluye
        - Posts
        - Comentarios
        - Likes en post y comentarios
        '''
        feed = self.get_page_posts()


        if 'error' in feed:
            return feed
        
        feed = self.modify_feed_timezone_response(feed, timezone)

        for post in feed.get('data'):
            # Ir a buscar los comentarios del post, con sus respectivos likes
            comments = self.get_post_comments(post.get('id')).get('data')
            for comment in comments:
                comment_likes = self.get_post_likes(comment.get('id'))
                comment['likes_amount'] = comment_likes.get('likes').get('summary').get('total_count')
                comment['users_that_liked'] = comment_likes.get('likes').get('data')

            # Agregar la key comments en el post
            post['comments'] = comments
            
            # Agregar información acerca de los likes del post
            likes = self.get_post_likes(post.get('id'))
            post['likes_amount'] = likes.get('likes').get('summary').get('total_count')
            post['users_that_liked'] = likes.get('likes').get('data')

        return feed
    

    def modify_feed_timezone_response(self, response_dict, user_timezone):
        '''
        Este método se encarga de devolver el mismo response_dict que recibe, pero modificando cada instancia
        de created_time usando la zona horaria del usuario
        '''
        for value in response_dict.get('data'):
            # obtener created time
            created_time = value.get('created_time')

            # modificar el string para que tenga formato 'iso'
            created_time = created_time[:-2] + ':' + created_time[-2:]

            created_time = datetime.fromisoformat(created_time).astimezone(timezone(user_timezone))

            value['created_time'] = str(created_time)        

        return response_dict


    def already_liked(self, comment):
        '''
        Devuelve true si alguno de los usuarios que dieron like coincide con el que nosotros buscamos
        '''
        return any([user.get('id') == self.page_id for user in comment.get('users_that_liked')])


    def make_post(self, message):
        '''
        Uso Facebook SDK para realizar un post que contiene un mensaje
        '''
        response = self.graph_api.put_object("me", "feed", message = message)
        print(f'Make post status: {response}')


    def make_post_image(self, image_path, message):
        '''
        Uso Facebook SDK para realizar un post que contiene una imagen y un mensaje 
        '''
        self.graph_api.put_photo(open(image_path, "rb"), message = message)


    def comment(self, post_id, message):
        '''
        Este método se encarga de publicar un comentario, el post_id puede ser el id de un post
        o el id de otro comentario, y la página hará una respuesta al comentario
        '''
        response = self.graph_api.put_object(str(post_id), "comments", message = message)
        print(f'Comment: Status {response}')


    def get_page_posts(self):
        '''
        Función que retorna todos los Post propios de una página
        '''
        url = f"https://graph.facebook.com/v13.0/{ str(self.page_id) }/posts?&access_token={ str(self.access_token) }&app_id=748013059515309"

        response = requests.get(url = url)

        return response.json()

    
    def get_post_comments(self, post_id):
        '''
        Obtener los comentarios de un post
        '''

        # HARDCODEADO
        url = f"https://graph.facebook.com/v13.0/{ str(post_id) }/comments?access_token={ str(self.access_token) }&app_id=748013059515309"

        response = requests.get(url = url)

        return response.json()


    def get_post_likes(self, post_id):
        '''
        Obtener todos los likes de un post (cantidad y usuarios que dieron like)
        '''

        # HARDCODEADO
        url = f"https://graph.facebook.com/{ str(post_id) }?fields=likes.summary(true)&access_token={ str(self.access_token) }&app_id=748013059515309"

        response = requests.get(url = url)

        return response.json()


    def send_message(self, recv_id, message_content):
        '''
        Función que recibe id del receptor del mensaje (recv_id) y contenido
        del mensaje (message_content) y envía el mensaje por privado al usuario.
        Esta función es usada para responder mensajes de messenger, no para responder por privado
        a comentarios de nuestras publicaciones
        '''
        payload = requests_tools.generate_message_payload(recv_id, message_content)
        header = requests_tools.application_json()

        response = requests.post(url = self.send_message_url, 
                    headers = header, 
                    data = payload)

        return response
    

    def private_reply(self, comment_id, message_content):
        '''
        Responder con un mensaje a alguien que haya comentado un post
        '''

        url = self.send_message_url

        header = requests_tools.application_json()
        payload = requests_tools.generate_private_reply_payload(comment_id, message_content)

        response = requests.post(url = url, headers = header, data = payload)
        print(f'Private reply: Status { response }')

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
        payload = requests_tools.generate_reply_button_payload(comment_id, message_content)

        requests.post(url = url, headers = header, data = payload)

    
    def put_like(self, object_id):
        '''
        Likear un objeto, con objeto, se hace referencia tanto a un post
        como a un comentario, o lo que sea que tenga un id, exceptuando un usuario u
        otra página
        '''
        self.graph_api.put_like(object_id = object_id)


    def already_answered(self, comment):
        '''
        Devuelve true si en las respuestas de un comentario hay respuestas de la página
        '''

        # Obtener respuestas del comentario
        replies = requests.get(
            f"https://graph.facebook.com/v13.0/{ str(comment.get('id')) }/comments?access_token={ str(self.access_token) }&app_id=748013059515309").json()
        
        for c in replies.get('data'):
            if c:
                if c.get('from'):
                    if c.get('from').get('id') == self.page_id:
                        return True

        return False
        # return any([replie.get('from').get('id') == self.page_id for replie in replies.get('data')])


    def get_profile_picture(self, id = None):
        '''
        Devuelve la foto de perfil de un usuario dado su ID
        '''

        # NOTE: Funcionalidad aún no implementada, devuelve valor hardcodeado

        # if id:
        #     url = f'https://graph.facebook.com/{id}/picture'

        #     data = requests.get(url)

        #     if data.status_code <= 400:
        #         return data.__dict__.get('url')

        #     return 'https://scontent.feze8-2.fna.fbcdn.net/v/t1.30497-1/84628273_176159830277856_972693363922829312_n.jpg?stp=c15.0.50.50a_cp0_dst-jpg_p50x50&_nc_cat=1&ccb=1-7&_nc_sid=12b3be&_nc_ohc=Jblb2zGGvosAX-qf9-a&_nc_ht=scontent.feze8-2.fna&edm=AHgPADgEAAAA&oh=00_AT_IwNVp-E8AmTv9GyemvAi0Jwc5521ZSng6gW7mM7ug8g&oe=62C07D99' # Imagen default

        return 'https://scontent.feze8-2.fna.fbcdn.net/v/t1.30497-1/84628273_176159830277856_972693363922829312_n.jpg?stp=c15.0.50.50a_cp0_dst-jpg_p50x50&_nc_cat=1&ccb=1-7&_nc_sid=12b3be&_nc_ohc=Jblb2zGGvosAX-qf9-a&_nc_ht=scontent.feze8-2.fna&edm=AHgPADgEAAAA&oh=00_AT_IwNVp-E8AmTv9GyemvAi0Jwc5521ZSng6gW7mM7ug8g&oe=62C07D99' # Imagen default
    

    def get_user_info_by_id(self, id):
        '''
        Devuelve el nombre de un usuario dado su ID
        @return {
            "first_name":<first_name>,
            "last_name":<last_name>,
            "profile_pic": <url>,
            "id":"5309191945779484"
        '''

        url = 'https://graph.facebook.com/' + str(id)
        params = {
            'access_token': self.access_token,
            'app_id': '748013059515309' # os.getenv('app_id')
        }

        print('REQUEST MADE:', url, params)

        response = requests.get(url = url, params = params).json()

        # HARDCODEADO
        response['profile_pic'] = 'https://scontent.feze8-2.fna.fbcdn.net/v/t1.30497-1/84628273_176159830277856_972693363922829312_n.jpg?stp=c15.0.50.50a_cp0_dst-jpg_p50x50&_nc_cat=1&ccb=1-7&_nc_sid=12b3be&_nc_ohc=Jblb2zGGvosAX-qf9-a&_nc_ht=scontent.feze8-2.fna&edm=AHgPADgEAAAA&oh=00_AT_IwNVp-E8AmTv9GyemvAi0Jwc5521ZSng6gW7mM7ug8g&oe=62C07D99' # Imagen default

        return response

    def get_unanswered_comments(self):
        '''
        Obtener todos los comentarios sin responder
        '''
        feed = self.get_feed()

        print(feed)

        cant_comentarios_sin_responder = 0

        for post in feed.get('data'):
            comments = post.get('comments')
            new_comments = []
            for comment in comments:
                if not self.already_answered(comment):

                    cant_comentarios_sin_responder += 1

                    try:
                        comment['owner'] = comment.get('from').get('name')
                        comment['picture'] = self.get_profile_picture(comment.get('from').get('id'))

                    except:
                        comment['owner'] = 'Unknown'
                        comment['picture'] = self.get_profile_picture(None)
                
                    new_comments.append(comment)
            
            post['comments'] = new_comments

        feed['cant_comentarios_sin_responder'] = cant_comentarios_sin_responder

        return feed
