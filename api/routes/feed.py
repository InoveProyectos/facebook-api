#!/usr/bin/env python

from flask import Blueprint, Response, request, jsonify, render_template
import traceback
from src.Facebook import *


# Blueprint que va a contener el endpoint para obtener los mensajes del feed
feed = Blueprint('feed', __name__, template_folder = '../templates')


@feed.route('/feed', methods = ['GET'])
def feed_get():
    try:
        return render_template('feed_form.html')

    except:
        return jsonify({'trace': traceback.format_exc()})


@feed.route('/feed', methods = ['POST'])
def feed_post():
    access_token = str(request.form.get('access_token'))
    page_id = str(request.form.get('page_id'))

    if not (access_token or page_id):
        print('No se enviaron los parámetros necesarios')
        return Response(status = 400) 

    fb = Facebook(access_token, page_id)

    feed = fb.get_feed()

    return jsonify(feed)
    

@feed.route('/answer-comment', methods = ['POST'])
def answer_comment():
    access_token = str(request.form.get('access_token'))
    page_id = str(request.form.get('page_id'))
    comment_id = str(request.form.get('comment_id'))
    answer = str(request.form.get('answer'))

    if not (access_token or page_id or comment_id or answer):
        print('No se enviaron los parámetros necesarios')
        return Response(status = 400) 
    
    fb = Facebook(access_token, page_id)

    fb.put_like(comment_id)
    fb.comment(comment_id, 'Te enviamos mas información por privado :)')
    response = fb.private_reply(comment_id, answer)
    
    return response