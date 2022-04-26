#!/usr/bin/env python

from flask import Blueprint, Response, request, jsonify
from src.Facebook import *


# Blueprint que va a contener el endpoint para obtener los mensajes del feed
feed = Blueprint('feed', __name__)


@feed.route('/feed', methods = ['GET'])
def feed_get():
    access_token = str(request.args.get('access_token'))
    page_id = str(request.args.get('page_id'))

    if not (access_token or page_id):
        print('No se enviaron los parámetros necesarios')
        return Response(status = 400) 

    fb = Facebook(access_token, page_id)

    feed = fb.get_feed()

    return jsonify(feed)
    