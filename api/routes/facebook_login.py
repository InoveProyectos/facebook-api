#!/usr/bin/env python

from flask import Blueprint, Response, request, jsonify, render_template, redirect, url_for
import traceback
from src.Facebook import *


# Blueprint que va a contener el endpoint para obtener los mensajes del feed
fb_login = Blueprint('login', __name__, template_folder = '../templates')


@fb_login.route('/login', methods = ['GET'])
def facebook_login():
    try:
        return render_template('facebook_login.html')

    except:
        return jsonify({'trace': traceback.format_exc()})
