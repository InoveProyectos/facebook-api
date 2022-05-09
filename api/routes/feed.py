#!/usr/bin/env python

from flask import Blueprint, Response, request, jsonify, redirect, url_for
from dotenv import load_dotenv
import os, sys, inspect

# Setear import path en directorio api
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.Facebook import *

# Cargar variables de entorno (archivo .env)
load_dotenv()

feed = Blueprint('feed', __name__)

@feed.route('/feed', methods = ['GET'])
def load_feed():
    body = request.form.to_dict()

    print(body)
    # user_id = body.get('userId')
    # access_token = body.get('accessToken')

    return jsonify(body)
